"""Strict read-only audit for the 2 GEN payout on submitted PlotPools."""
import json
from genlayer_py.types import TransactionHashVariant

def verify_submitted_pool(c,p,receipts):
    amount=2*10**18;demo=p.get('submittedPoolDemo')
    assert demo and demo.get('status')=='PAID','Submitted PlotPools 2 GEN payout is not yet proved'
    address=p['contracts']['PlotPools']['address'];wallet=demo['wallet'];key=demo['marketId']
    assert demo['poolAddress']==address and int(demo['approvedDepositWei'])==amount
    def read(method,args):
        value=c.read_contract(address,method,args=args,transaction_hash_variant=TransactionHashVariant.LATEST_FINAL)
        return json.loads(value) if isinstance(value,str) else value
    pool=read('get_pool',[key]);account=read('get_account',[key,wallet])
    assert pool['status']=='SETTLED' and pool['mode']=='REHEARSAL' and pool['total']==amount
    assert sum(pool['payouts'].values())==amount and pool['payouts'][wallet]==amount
    assert pool['entries'][wallet]=={'option':demo['winningOption'],'amount':amount}
    claim=account['claim'];assert claim['status']=='PAID' and claim['amount']==amount
    required=['compile','compile-child-0','resolve','resolve-child-0','prepare','deposit','settle','settle-child-0','claim','claim-child-0','verify']
    assert all('submitted-2gen-'+label in receipts for label in required),'Missing finalized submitted-pool receipt'
    for label in ['compile','resolve','prepare','deposit','settle','claim','verify']:
        target=p['contracts']['PlotMarkets' if label=='compile' else 'PlotResolver' if label=='resolve' else 'PlotPools']['address']
        row=receipts['submitted-2gen-'+label]
        assert row['from_address'].lower()==wallet.lower() and row['to_address'].lower()==target.lower(),'Wrong write sender or target: '+label
        assert int(row['value'])==(amount if label=='deposit' else 0),'Wrong native write value: '+label
    for label in ['compile','resolve','settle']:
        parent=receipts['submitted-2gen-'+label];callback=receipts['submitted-2gen-'+label+'-child-0']
        assert callback['hash'] in parent['triggered_transactions'] and callback['triggered_by']==parent['hash']
        assert callback['to_address'].lower()==parent['to_address'].lower() and callback['from_address'].lower()==parent['to_address'].lower()
    parent=receipts['submitted-2gen-claim'];child=receipts['submitted-2gen-claim-child-0']
    assert claim['parent']==parent['hash'] and claim['child']==child['hash']
    assert child['hash'] in parent['triggered_transactions'] and child['triggered_by']==parent['hash']
    assert child['value_credited'] is True and int(child['value'])==amount
    assert child['from_address'].lower()==address.lower() and child['to_address'].lower()==wallet.lower()
    deposit=receipts['submitted-2gen-deposit'];assert int(deposit['value'])==amount and deposit['to_address'].lower()==address.lower()
    balances=demo['balances'];start=balances['before_stake'];w=int(start['walletWei']);b=int(start['poolWei'])
    funding=receipts['submitted-2gen-funding']
    assert funding['value_credited'] is True and int(funding['value'])==amount and funding['to_address'].lower()==wallet.lower()
    assert w==int(p['payoutUpgrade']['preflightWalletBalanceWei'])+amount and b==int(p['payoutUpgrade']['preflightPoolBalanceWei'])
    for stage,expected in [('after_deposit',(w-amount,b+amount)),('after_settlement',(w-amount,b+amount)),('after_native_credit',(w,b)),('after_verified_paid',(w,b))]:
        row=balances[stage];assert (int(row['walletWei']),int(row['poolWei']))==expected,'Recorded balance arithmetic mismatch: '+stage
    for who,expected in [(wallet,w),(address,b)]:
        actual=c.provider.make_request('eth_getBalance',[who,'latest'])['result']
        assert int(actual,16)==expected,'Native balance differs from verified post-claim balance'
    print('PASS: submitted PlotPools 2 GEN stake, finalized payout, PAID native credit and exact wallet/pool balances verified.',flush=True)
