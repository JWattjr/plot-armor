"""Read-only: no secrets, signer, faucet, transaction submission or file writes."""
import ast
import argparse
import base64
import hashlib
import json
import subprocess
import time
from pathlib import Path
from html import unescape
import re
from datetime import datetime,timezone
from urllib.parse import quote
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from eth_account import Account
from genlayer_py import create_client,studionet
from genlayer_py.provider import provider
from genlayer_py.types import TransactionHashVariant

ROOT=Path(__file__).resolve().parent.parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--proof',default='deploy/proof.json',help='Proof manifest to audit; all mandatory checks still apply.')
args=parser.parse_args()
p=json.loads((ROOT/args.proof).read_text(encoding='utf8'))
post=provider.requests.post
last=0
def browser_post(url,**kwargs):
    global last
    time.sleep(max(0,2.6-(time.monotonic()-last)));last=time.monotonic()
    kwargs['headers']={**kwargs.get('headers',{}),'User-Agent':'Mozilla/5.0 PlotArmorProof/1.0'}
    kwargs.setdefault('timeout',60)
    return post(url,**kwargs)
provider.requests.post=browser_post
# gen_call needs a caller, but this ephemeral account never signs anything.
c=create_client(chain=studionet,account=Account.create())
def read(name,method,args):
    v=c.read_contract(p['contracts'][name]['address'],method,args=args,transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    return json.loads(v) if isinstance(v,str) else v
def receipt(h):
    r=c.provider.make_request('eth_getTransactionByHash',[h])['result']
    assert r and r['status']=='FINALIZED',f'Not finalized: {h}'
    if r.get('type')==0 and r.get('consensus_data') is None:
        assert r.get('value_credited') is True,'Native credit missing'
    else:
        leader=((r.get('consensus_data') or {}).get('leader_receipt') or [{}])[0]
        assert leader.get('execution_result')=='SUCCESS' and r.get('result_name') in (None,'AGREE','MAJORITY_AGREE','SUCCESS'),f'Finalized error: {h}'
    return r
def main():
    assert len(p['contracts'])==4,'Four contracts not yet recorded'
    assert p.get('sourceCommit'),'Source commit missing'
    assert subprocess.check_output(['git','cat-file','-t',p['sourceCommit']],cwd=ROOT,text=True).strip()=='commit'
    links=json.loads(subprocess.check_output(['node','--import','tsx','scripts/links.ts',str(ROOT/args.proof)],cwd=ROOT,text=True))
    session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 PlotArmorProof/1.0'
    session.mount('https://',HTTPAdapter(max_retries=Retry(total=2,backoff_factor=2,status_forcelist=[429,500,502,503,504],allowed_methods=['GET'])))
    for name,contract in p['contracts'].items():
        source=(ROOT/'contracts'/contract['source']).read_text(encoding='utf8').encode('utf8')
        assert hashlib.sha256(source).hexdigest()==contract['sourceSha256'],'Local source hash mismatch'
        committed=subprocess.check_output(['git','show',p['sourceCommit']+':contracts/'+contract['source']],cwd=ROOT)
        assert hashlib.sha256(committed).hexdigest()==contract['sourceSha256'],'Source commit does not contain deployed source'
        deployed=c.provider.make_request('gen_getContractCode',[contract['address']])['result']
        raw=base64.b64decode(deployed) if isinstance(deployed,str) else bytes(deployed)
        assert raw==source,'Deployed source differs: '+name
        response=session.get(links['contracts'][name]['api'],timeout=40);response.raise_for_status();record=response.json()
        assert record.get('type')=='CONTRACT','Explorer does not identify CONTRACT: '+name
        print('CONTRACT verified',name,links['contracts'][name]['page'],flush=True)
    receipts={}
    for name,h in p['transactions'].items():
        receipts[name]=receipt(h)
        response=session.get(links['transactions'][name]['api'],timeout=40);response.raise_for_status();data=response.json()
        text=json.dumps(data).lower()
        assert h.lower() in text,'Explorer transaction record mismatch: '+name
        print('FINALIZED_SUCCESS + explorer',name,h,flush=True)
    # Execute the actual deployed deterministic parser, without loading GenVM.
    source=ast.parse((ROOT/'contracts/plot_resolver.py').read_text())
    functions=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in ('clean','templates','extract_summary','summary_digest')]
    scope={'re':re,'unescape':unescape,'hashlib':hashlib}
    exec(compile(ast.Module(body=functions,type_ignores=[]),'<deployed-parser>','exec'),scope)
    compiler=ast.parse((ROOT/'contracts/plot_markets.py').read_text(encoding='utf8'))
    metadata_functions=[n for n in compiler.body if isinstance(n,ast.FunctionDef) and n.name in ('clean','templates','compilation_metadata','extraction_path_exists')]
    metadata_scope={'re':re,'unescape':unescape}
    exec(compile(ast.Module(body=metadata_functions,type_ignores=[]),'<deployed-metadata-parser>','exec'),metadata_scope)
    outcomes=[]
    for saved in p['markets']:
        m=read('PlotMarkets','get_market',[saved['id']])
        assert all(m[k]==saved[k] for k in m),'Recorded compile differs from live finalized state'
        if not m['accepted']:
            assert m['status']=='REJECTED';continue
        assert hashlib.sha256(json.dumps(m['spec'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==m['spec_hash']
        spec=m['spec'];revision=spec['source_revision']
        cutoff=datetime.fromtimestamp(m['created_at'],timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        response=session.get('https://en.wikipedia.org/w/api.php',params={'action':'query','format':'json','prop':'revisions','rvprop':'ids','rvdir':'older','rvlimit':1,'rvstart':cutoff,'titles':spec['article']},timeout=40);response.raise_for_status()
        page=next(iter(response.json()['query']['pages'].values()))
        assert page['ns']==0 and page['revisions'][0]['revid']==revision,'Compile metadata revision was not selected by code at proposal time'
        metadata_url=links['metadata'][m['id']]
        response=session.get(metadata_url,timeout=45);response.raise_for_status();text=response.content.decode('utf8')[:65000]
        assert hashlib.sha256(text.encode()).hexdigest()==spec['source_digest'],'Pinned compiler metadata digest differs'
        assert metadata_scope['extraction_path_exists'](metadata_scope['compilation_metadata'](text,spec['episode']),spec),'Frozen extraction path does not exist'
        print('Pinned compile metadata and extraction path verified',m['id'],revision,flush=True)
        r=read('PlotResolver','get_resolution',[m['id']])
        assert r==saved.get('resolution',{}),'Recorded resolution differs'
        if r.get('status')=='RESOLVED':
            response=session.get(r['url'],timeout=45);response.raise_for_status()
            summary=scope['extract_summary'](response.text,m['spec'])
            assert scope['summary_digest'](summary)==r['digest'] and r['quote'] in summary and 8<=len(r['quote'])<=400
            assert r['revision_utc']>=m['spec']['air_utc']+172800
            start=datetime.fromtimestamp(m['spec']['air_utc']+172800,timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            params={'action':'query','format':'json','prop':'revisions','titles':m['spec']['article'],'rvprop':'ids|timestamp','rvdir':'newer','rvstart':start,'rvlimit':5}
            first=None
            for page_index in range(20):
                api=session.get('https://en.wikipedia.org/w/api.php',params=params,timeout=40);api.raise_for_status();listing=api.json()
                revisions=next(iter(listing['query']['pages'].values())).get('revisions',[])
                for revision in revisions:
                    url='https://en.wikipedia.org/w/index.php?title='+quote(m['spec']['article'],safe='')+'&oldid='+str(revision['revid'])+'&action=raw'
                    raw=session.get(url,timeout=40);raw.raise_for_status()
                    if scope['extract_summary'](raw.text,m['spec']):
                        first=revision['revid'];break
                if first is not None or 'continue' not in listing:break
                params['rvcontinue']=listing['continue']['rvcontinue']
            assert first==r['revision'],'Not the earliest eligible revision containing this summary'
            outcomes.append((m['spec']['options'],r['outcome']))
            print('Immutable evidence digest and verbatim quote verified',m['id'],r['revision'],flush=True)
    demo=p.get('poolDemo');assert demo and demo['approvedDepositWei']=='11','Approved pool proof missing'
    pool_address=p['contracts']['PlotPools']['address']
    if demo.get('legacyContracts'):
        legacy=demo['legacyContracts']['PlotPools'];pool_address=legacy['address']
        committed=subprocess.check_output(['git','show',demo['sourceCommit']+':contracts/'+legacy['source']],cwd=ROOT)
        assert hashlib.sha256(committed).hexdigest()==legacy['sourceSha256']==p['contracts']['PlotPools']['sourceSha256'],'Archived payout must use the identical pool implementation'
        deployed=c.provider.make_request('gen_getContractCode',[pool_address])['result']
        assert base64.b64decode(deployed)==committed,'Archived pool source mismatch'
        legacy_api=links['legacyContracts']['PlotPools']['api']
        response=session.get(legacy_api,timeout=40);response.raise_for_status();assert response.json().get('type')=='CONTRACT'
        print('Archived identical pool implementation and CONTRACT record verified',pool_address,flush=True)
    def pool_read(method,args):
        value=c.read_contract(pool_address,method,args=args,transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
        return json.loads(value) if isinstance(value,str) else value
    pool=pool_read('get_pool',[demo['marketId']]);account=pool_read('get_account',[demo['marketId'],demo['wallet']])
    assert pool['status']=='SETTLED' and pool['total']==11 and sum(pool['payouts'].values())==11
    assert account['claim']['status']=='PAID' and account['claim']['amount']==11
    claim=account['claim'];parent=receipt(claim['parent']);child=receipt(claim['child'])
    assert child['hash'] in parent['triggered_transactions'] and child['value_credited'] is True and int(child['value'])==11
    assert child['to_address'].lower()==demo['wallet'].lower()
    print('Native pool allocation and credited 11-wei claim verified.',flush=True)
    free=p.get('freeDemo');assert free,'Missing real free prediction demo'
    predictions=read('PlotSeasons','get_predictions',[free['wallet']])
    assert predictions==free['predictions'],'Recorded free predictions differ'
    prediction=next(row for row in predictions if row['market']==free['marketId'])
    market=next(m for m in p['markets'] if m['id']==free['marketId'])
    assert not prediction['rehearsal'] and prediction['season']==free['season']==market['spec']['show']+' / S'+str(market['spec']['season'])
    for season,key in [('', 'leaderboard'),(free['season'],'seasonLeaderboard')]:
        actual=read('PlotSeasons','leaderboard',[season])
        assert next(row for row in actual if row['wallet']==free['wallet'])==next(row for row in free[key] if row['wallet']==free['wallet']),'Recorded demo leaderboard row differs'
    adapter=json.loads((ROOT/'deploy/wallet-adapter-check.json').read_text(encoding='utf8'))
    assert adapter['state']=='FINALIZED_SUCCESS' and adapter['valueWei']=='0' and adapter['hash']==p['transactions']['predict-live-free']
    transaction=receipts['predict-live-free']
    assert transaction['from_address'].lower()==free['wallet'].lower() and transaction['to_address'].lower()==p['contracts']['PlotSeasons']['address'].lower() and int(transaction['value'])==0
    print('Real Node EIP-1193 adapter prediction and overall/season leaderboard rows verified; extension popup is outside this check.',flush=True)
    if p.get('browserDemo'):
        from verify_browser import verify_browser
        verify_browser(c,p,session,receipts['predict-browser-metamask'])
    assert any(o==['YES','NO'] and i==0 for o,i in outcomes),'Missing YES demo'
    assert any(o==['YES','NO'] and i==1 for o,i in outcomes),'Missing NO demo'
    assert any(o!=['YES','NO'] for o,i in outcomes),'Missing multiple-choice demo'
    assert any(not m['accepted'] and m['status']=='REJECTED' for m in p['markets']),'Missing rejected proposal'
    assert len([m for m in p['markets'] if m.get('spec') and not m['spec']['rehearsal'] and m['status']=='OPEN'])>=1,'Missing live market'
    print('PASS: all four sources, finalized receipts, permanent evidence, real explorer records, YES/NO/choice/rejection, live markets and 11-wei native claim verified.')
if __name__=='__main__':main()
