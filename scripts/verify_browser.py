"""Read-only verification of the owner's real MetaMask prediction."""
import json
from pathlib import Path

def verify_browser(c,p,session,transaction=None):
    demo=p['browserDemo'];h=demo['hash']
    r=transaction or c.provider.make_request('eth_getTransactionByHash',[h])['result']
    assert r and r['status']=='FINALIZED'
    leader=((r.get('consensus_data') or {}).get('leader_receipt') or [{}])[0]
    assert leader.get('execution_result')=='SUCCESS' and r.get('result_name') in (None,'AGREE','MAJORITY_AGREE','SUCCESS')
    assert int(r['value'])==0 and r['to_address'].lower()==p['contracts']['PlotSeasons']['address'].lower()
    wallet=r['from_address'].lower()
    from genlayer_py.types import TransactionHashVariant
    value=c.read_contract(p['contracts']['PlotSeasons']['address'],'get_predictions',args=[wallet],transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
    predictions=json.loads(value) if isinstance(value,str) else value
    row=next(row for row in predictions if row['market']==demo['marketId'])
    assert row['option']==demo['option'] and not row['rehearsal']
    # Use the same canonical link builder as the application and main audit.
    import subprocess
    root=Path(__file__).resolve().parent.parent
    links=json.loads(subprocess.check_output(['node','--import','tsx','scripts/links.ts'],cwd=root,text=True))
    api=links['transactions']['predict-browser-metamask']['api']
    response=session.get(api,timeout=40);response.raise_for_status()
    assert h.lower() in json.dumps(response.json()).lower()
    print('PASS: real owner-signed MetaMask prediction finalized successfully; value 0, correct contract, finalized personal prediction and explorer record verified.',flush=True)
    return {'wallet':wallet,'state':'FINALIZED_SUCCESS','predictions':predictions,'receipt':r}

if __name__=='__main__':
    import requests
    from eth_account import Account
    from genlayer_py import create_client,studionet
    from chain import ROOT
    p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
    c=create_client(chain=studionet,account=Account.create())
    session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 PlotArmorProof/1.0'
    result=verify_browser(c,p,session)
    (ROOT/'deploy/browser-wallet-check.json').write_text(json.dumps(result,indent=2)+'\n')
