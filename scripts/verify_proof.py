"""Read-only: no secrets, signer, faucet, transaction submission or file writes."""
import ast
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
from eth_account import Account
from genlayer_py import create_client,studionet
from genlayer_py.provider import provider
from genlayer_py.types import TransactionHashVariant

ROOT=Path(__file__).resolve().parent.parent
p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
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
    links=json.loads(subprocess.check_output(['node','--import','tsx','scripts/links.ts'],cwd=ROOT,text=True))
    session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 PlotArmorProof/1.0'
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
    outcomes=[]
    for saved in p['markets']:
        m=read('PlotMarkets','get_market',[saved['id']])
        assert all(m[k]==saved[k] for k in m),'Recorded compile differs from live finalized state'
        if not m['accepted']:
            assert m['status']=='REJECTED';continue
        assert hashlib.sha256(json.dumps(m['spec'],sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==m['spec_hash']
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
    pool=read('PlotPools','get_pool',[demo['marketId']]);account=read('PlotPools','get_account',[demo['marketId'],demo['wallet']])
    assert pool['status']=='SETTLED' and pool['total']==11 and sum(pool['payouts'].values())==11
    assert account['claim']['status']=='PAID' and account['claim']['amount']==11
    claim=account['claim'];parent=receipt(claim['parent']);child=receipt(claim['child'])
    assert child['hash'] in parent['triggered_transactions'] and child['value_credited'] is True and int(child['value'])==11
    assert child['to_address'].lower()==demo['wallet'].lower()
    print('Native pool allocation and credited 11-wei claim verified.',flush=True)
    assert any(o==['YES','NO'] and i==0 for o,i in outcomes),'Missing YES demo'
    assert any(o==['YES','NO'] and i==1 for o,i in outcomes),'Missing NO demo'
    assert any(o!=['YES','NO'] for o,i in outcomes),'Missing multiple-choice demo'
    assert any(not m['accepted'] and m['status']=='REJECTED' for m in p['markets']),'Missing rejected proposal'
    assert len([m for m in p['markets'] if m.get('spec') and not m['spec']['rehearsal'] and m['status']=='OPEN'])>=1,'Missing live market'
    print('PASS: all four sources, finalized receipts, permanent evidence, real explorer records, YES/NO/choice/rejection, live markets and 11-wei native claim verified.')
if __name__=='__main__':main()
