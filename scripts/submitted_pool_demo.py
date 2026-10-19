"""One authorized 2 GEN payout on the existing submitted contracts. No deploys.

Supply the owner's finalized native funding hash. All submitted hashes are saved
before polling. Rerun the same command after a polling timeout; never relabel a
failed write or replace a saved hash. Contract/state failures halt the run.
"""
import argparse,json,time
from datetime import datetime,timezone
from decimal import Decimal
from chain import ROOT,client,signer,read,transaction,final,save

A=2*10**18
EXPECTED={
 'PlotMarkets':'0xAE26C101532f706265FFc56dbD1C411062E66628',
 'PlotResolver':'0x311413A6c4f6534Dfb843E44dBf594d37ecdAf1c',
 'PlotPools':'0xcFC2062bFab042e9885f58c44a2B8e2Ce061e792',
 'PlotSeasons':'0x970E83e7CeFC869FAF3e73D2E2EA28F76A26FfFB'}
QUESTION='In Ozymandias (broadcast 2013-09-15T21:00:00-04:00), does Hank Schrader die? Answer YES or NO.'

def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--funding-hash',required=True);args=parser.parse_args()
 p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'));c=client();wallet=signer().address.lower()
 assert all(p['contracts'][n]['address']==v for n,v in EXPECTED.items()),'Submitted contract identity changed'
 demo=p.setdefault('submittedPoolDemo',{'approvedDepositWei':str(A),'approvedDepositGEN':'2','approvalSource':'Owner explicitly requested a 2 GEN stake on the submitted PlotPools','wallet':wallet,'poolAddress':EXPECTED['PlotPools'],'balances':{},'fundingHash':args.funding_hash})
 assert demo['wallet']==wallet and demo['fundingHash']==args.funding_hash and demo['approvedDepositWei']==str(A)
 assert not demo.get('halted'),'A prior execution/state failure requires owner review; no resubmission'
 p['submissionReady']=False;p['blockers']=['Submitted-pool 2 GEN payout verification in progress.'];save(p)
 def balance(address):
  result=c.provider.make_request('eth_getBalance',[address,'latest']);assert not result.get('error'),result
  return int(result['result'],16)
 def snapshot(label,expected=None):
  if label in demo['balances']:return demo['balances'][label]
  w=balance(wallet);pool=balance(EXPECTED['PlotPools'])
  row={'walletWei':str(w),'poolWei':str(pool),'walletGEN':format(Decimal(w)/10**18,'f'),'poolGEN':format(Decimal(pool)/10**18,'f'),'at':datetime.now(timezone.utc).isoformat()}
  if expected is not None:assert (w,pool)==expected,f'Balance mismatch at {label}: {row}; expected {expected}'
  demo['balances'][label]=row;save(p);print('BALANCE',label,json.dumps(row),flush=True);return row
 def invoke(label,name,method,values,value=0):
  demo['stage']=label;save(p)
  return transaction(c,p,'submitted-2gen-'+label,EXPECTED[name],method,values,value=value)
 try:
  funding=final(c,args.funding_hash,'submitted-2gen-funding')
  assert funding['type']==0 and funding.get('value_credited') is True and int(funding['value'])==A and funding['to_address'].lower()==wallet,'Wrong native funding transfer'
  p['transactions']['submitted-2gen-funding']=args.funding_hash;save(p)
  initial=snapshot('before_stake');base=int(initial['walletWei']);pool_base=int(initial['poolWei']);assert base>=A
  if 'idsBefore' not in demo:demo['idsBefore']=read(c,EXPECTED['PlotMarkets'],'get_ids');save(p)
  invoke('compile','PlotMarkets','rehearse',[QUESTION,'Breaking Bad',5,14])
  if 'marketId' not in demo:
   ids=read(c,EXPECTED['PlotMarkets'],'get_ids');created=[key for key in ids if key not in demo['idsBefore']];assert len(created)==1,'Inspect new market identity before resuming'
   demo['marketId']=created[0];save(p)
  key=demo['marketId'];market=read(c,EXPECTED['PlotMarkets'],'get_market',[key])
  assert market['accepted'] and market['status']=='OPEN' and market['creator']==wallet and market['spec']['rehearsal'],'Historical rehearsal was not accepted for this owner'
  invoke('resolve','PlotResolver','resolve',[key]);resolution=read(c,EXPECTED['PlotResolver'],'get_resolution',[key])
  assert resolution['status']=='RESOLVED' and resolution['spec_hash']==market['spec_hash'],'Historical outcome did not resolve'
  winner=resolution['outcome'];assert type(winner) is int and market['spec']['options'][winner]=='YES'
  demo['winningOption']=winner;save(p)
  if 'submitted-2gen-prepare' not in p['transactions']:
   assert time.time()+300<market['spec']['entry_deadline'],'Insufficient rehearsal entry time; stop without depositing'
  invoke('prepare','PlotPools','prepare_stake',[key,winner,A])
  if 'ticket' not in demo:
   receipt=json.loads((ROOT/'deploy/receipts/submitted-2gen-prepare.json').read_text(encoding='utf8'))
   from genlayer_py.abi.calldata import decode
   import base64
   raw=(receipt['consensus_data']['leader_receipt'][0]['result'])
   payload=base64.b64decode(raw);assert payload[0]==0,'Stake ticket return is not a success value'
   decoded=decode(payload[1:]);assert isinstance(decoded,str) and decoded.startswith('ticket-'),repr(decoded)
   demo['ticket']=decoded;save(p)
  ticket=read(c,EXPECTED['PlotPools'],'get_ticket',[demo['ticket']])
  if 'submitted-2gen-deposit' not in p['transactions']:
   assert ticket['wallet']==wallet and ticket['market']==key and ticket['amount']==A and ticket['option']==winner and not ticket['used'] and time.time()<ticket['expires'],'Stake ticket is not valid'
  invoke('deposit','PlotPools','deposit',[demo['ticket']],value=A)
  pool=read(c,EXPECTED['PlotPools'],'get_pool',[key]);assert pool['total']==A and pool['entries'][wallet]=={'option':winner,'amount':A},'Deposit did not stake exactly 2 GEN'
  snapshot('after_deposit',(base-A,pool_base+A))
  if 'submitted-2gen-settle' not in p['transactions']:
   while time.time()<market['spec']['entry_deadline']:time.sleep(min(10,market['spec']['entry_deadline']-time.time()))
  invoke('settle','PlotPools','settle',[key]);pool=read(c,EXPECTED['PlotPools'],'get_pool',[key]);assert pool['status']=='SETTLED' and pool['payouts'][wallet]==A
  snapshot('after_settlement',(base-A,pool_base+A))
  invoke('claim','PlotPools','claim',[key,1]);account=read(c,EXPECTED['PlotPools'],'get_account',[key,wallet]);assert account['claim']['status'] in ('PENDING','PAID') and account['claim']['amount']==A
  snapshot('after_native_credit',(base,pool_base))
  parent=p['transactions']['submitted-2gen-claim'];child=p['transactions']['submitted-2gen-claim-child-0']
  native=final(c,child,'submitted-2gen-claim-child-0');assert native.get('value_credited') is True and int(native['value'])==A and native['to_address'].lower()==wallet
  invoke('verify','PlotPools','verify_claim',[key,wallet,1,parent,child]);account=read(c,EXPECTED['PlotPools'],'get_account',[key,wallet]);assert account['claim']['status']=='PAID' and account['claim']['amount']==A
  snapshot('after_verified_paid',(base,pool_base))
  demo.update({'account':account,'pool':pool,'status':'PAID','verifyCallback':'verify_claim updates verified status directly; it emits no callback','completedAt':datetime.now(timezone.utc).isoformat()})
  if p.get('poolDemo',{}).get('legacyContracts'):p.setdefault('previousPoolDemos',[]).append(p['poolDemo'])
  p['poolDemo']={**demo,'marketId':key};market['resolution']=resolution;market['pool']=pool;p['markets']=[m for m in p['markets'] if m['id']!=key]+[market];save(p)
  print('PAID: submitted PlotPools returned exactly 2 GEN with verified native credit.',flush=True)
 except Exception as error:
  demo['lastError']=str(error);demo['halted']='Finalized execution failed:' in str(error) or isinstance(error,AssertionError);save(p);raise

if __name__=='__main__':main()
