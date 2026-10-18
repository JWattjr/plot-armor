import json,pytest
from support import *
from conftest import to_hex
@pytest.fixture
def pool(direct_vm,direct_deploy,direct_owner,monkeypatch):
    direct_vm._chain_id=61999;direct_vm.sender=direct_owner;warp(direct_vm,T)
    c=direct_deploy('contracts/plot_pools.py',A,B);s=spec();state={'market':{'status':'OPEN','spec':s,'spec_hash':'frozen','creator':to_hex(direct_owner).lower()},'resolution':{'status':'RESOLVED','spec_hash':'frozen','outcome':0}}
    stub(monkeypatch,state);return c,state

def deposit(c,vm,option=0,amount=1):
    ticket=c.prepare_stake('m',option,amount);vm.value=amount;c.deposit(ticket);vm.value=0;return ticket

def test_wei_and_double_deposit_credit(pool,direct_vm):
    c,_=pool;ticket=deposit(c,direct_vm,amount=11);direct_vm.value=11;assert c.deposit(ticket)=='REFUND_CREDIT';direct_vm.value=0
    assert json.loads(c.get_pool('m'))['total']==11
    assert json.loads(c.get_account('m',to_hex(direct_vm.sender)))['credit']=='11'

@pytest.mark.parametrize('reason',['expired','wrong-amount','wrong-wallet','missing'])
def test_invalid_deposits_refundable(pool,direct_vm,direct_bob,reason):
    c,_=pool;ticket=c.prepare_stake('m',0,3)
    if reason=='expired':warp(direct_vm,T+100)
    if reason=='wrong-wallet':direct_vm.sender=direct_bob
    if reason=='missing':ticket='missing'
    direct_vm.value=2 if reason=='wrong-amount' else 3
    assert c.deposit(ticket)=='REFUND_CREDIT';amount=direct_vm.value;direct_vm.value=0
    assert int(json.loads(c.get_account('m',to_hex(direct_vm.sender)))['credit'])==amount

@pytest.mark.parametrize('mode',['void','empty','timeout'])
def test_refunds(pool,direct_vm,mode):
    c,state=pool;wallet=to_hex(direct_vm.sender).lower();deposit(c,direct_vm,amount=11);warp(direct_vm,T+100)
    if mode=='void':state['resolution']['status']='VOID'
    if mode=='empty':state['resolution']['outcome']=1
    if mode=='timeout':state['resolution']={};warp(direct_vm,T+200)
    c.settle('m');self_call(direct_vm,c.finalize_pool,'m');assert json.loads(c.get_pool('m'))['payouts'][wallet]==11

def test_pro_rata_remainders(pool,direct_vm,direct_bob,direct_charlie):
    c,_=pool;deposit(c,direct_vm,0,1);direct_vm.sender=direct_bob;deposit(c,direct_vm,0,2);direct_vm.sender=direct_charlie;deposit(c,direct_vm,1,4);warp(direct_vm,T+100);c.settle('m');self_call(direct_vm,c.finalize_pool,'m')
    r=json.loads(c.get_pool('m'));assert sorted(r['payouts'].values())==[0,2,5] and sum(r['payouts'].values())==7

def test_deadline_and_unfinalized_source(pool,direct_vm):
    c,state=pool;deposit(c,direct_vm)
    with direct_vm.expect_revert('entries still open'):c.settle('m')
    warp(direct_vm,T+100);state['resolution']['status']='PENDING_FINALITY'
    with direct_vm.expect_revert('result pending'):c.settle('m')
    with direct_vm.expect_revert('entries closed'):c.prepare_stake('m',0,1)

def test_claim_pending_blocks_double_and_unauthorized_callback(pool,direct_vm,direct_owner,monkeypatch):
    c,_=pool;deposit(c,direct_vm,amount=11);warp(direct_vm,T+100);c.settle('m');self_call(direct_vm,c.finalize_pool,'m')
    # Stub only the native emission, never payout arithmetic or claim state.
    import sys
    module=sys.modules['_contract_plot_pools']
    class Native:
        def __init__(self,*args):pass
        def emit_transfer(self,**kwargs):pass
    monkeypatch.setattr(module,'Recipient',Native)
    direct_vm.deal(direct_vm._contract_address,11)
    c.claim('m',1)
    assert json.loads(c.get_account('m',to_hex(direct_owner)))['claim']['status']=='PENDING'
    with direct_vm.expect_revert('claim already'):c.claim('m',2)
    with direct_vm.expect_revert('self finality'):c.finalize_pool('m')

def test_allocation_math_exhaustive(pool):
    fn=helpers('contracts/plot_pools.py')['allocation']
    for a in range(1,6):
        for b in range(1,6):
            p={'status':'RESOLVED','winner':0,'sides':[a+b,7],'total':a+b+7,'entries':{'a':{'option':0,'amount':a},'b':{'option':0,'amount':b},'c':{'option':1,'amount':7}}}
            v=fn(p);assert sum(v.values())==p['total'] and v['c']==0


def test_failed_credited_payable_recovery_and_replay(pool,direct_vm,monkeypatch):
    c,_=pool
    import sys
    module=sys.modules['_contract_plot_pools'];w=to_hex(direct_vm.sender).lower();contract=to_hex(direct_vm._contract_address).lower();h='0x'+'ab'*32
    r={'status':'FINALIZED','value_credited':True,'from_address':w,'to_address':contract,'value':11,'consensus_data':{'leader_receipt':[{'execution_result':'ERROR'}]}}
    monkeypatch.setattr(module,'receipt',lambda _:r)
    c.recover_failed_deposit(h)
    assert json.loads(c.get_account('credits',w))['credit']=='11'
    with direct_vm.expect_revert('already recovered'):c.recover_failed_deposit(h)

def test_successful_deposit_cannot_be_recovered(pool,direct_vm,monkeypatch):
    c,_=pool
    import sys
    module=sys.modules['_contract_plot_pools'];w=to_hex(direct_vm.sender).lower();contract=to_hex(direct_vm._contract_address).lower()
    r={'status':'FINALIZED','value_credited':True,'from_address':w,'to_address':contract,'value':11,'consensus_data':{'leader_receipt':[{'execution_result':'SUCCESS'}]}}
    monkeypatch.setattr(module,'receipt',lambda _:r)
    with direct_vm.expect_revert('only failed'):c.recover_failed_deposit('0x'+'ab'*32)
