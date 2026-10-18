import json,pytest
from support import *
@pytest.fixture
def market(direct_vm,direct_deploy,direct_owner,monkeypatch):
    direct_vm.sender=direct_owner;warp(direct_vm,T)
    c=direct_deploy('contracts/plot_markets.py');stub(monkeypatch,{'market':{}})
    direct_vm.mock_web(r'.*list=search.*',{'status':200,'body':json.dumps({'query':{'search':[{'title':'Test Show (season 1)'}]}})})
    direct_vm.mock_web(r'.*prop=revisions.*',{'status':200,'body':json.dumps({'query':{'pages':{'1':{'revisions':[{'slots':{'main':{'*':'Episode list for The Turn, Alex survives.'}}}]}}}})})
    return c

def answer(vm,accepted=True,**changes):
    s=spec();[s.pop(k) for k in ['rehearsal','entry_deadline','resolution_deadline']];s.update(changes)
    vm.mock_llm(r'.*PLOT_ARMOR_COMPILE\..*',json.dumps({'accepted':accepted,'reason':'Objective and well-defined.' if accepted else 'Subjective question.','spec':s if accepted else None}))

def test_accept_freeze_and_self_callback(market,direct_vm):
    answer(direct_vm);key=market.propose('Does Alex survive?','Test Show',1,1)
    r=json.loads(market.get_market(key));assert r['status']=='PENDING_FINALITY' and len(r['spec_hash'])==64
    with direct_vm.expect_revert('self finality'):market.finalize_compile(key)
    self_call(direct_vm,market.finalize_compile,key);r=json.loads(market.get_market(key));assert r['status']=='OPEN' and r['spec']['entry_deadline']<r['spec']['air_utc']

def test_reject_subjective(market,direct_vm):
    answer(direct_vm,False);key=market.propose('Is the episode good?','Test Show',1,1);self_call(direct_vm,market.finalize_compile,key)
    assert json.loads(market.get_market(key))['status']=='REJECTED'

def test_already_aired_is_rejected(market,direct_vm):
    answer(direct_vm,air_utc=T-1);key=market.propose('Does Alex survive?','Test Show',1,1);self_call(direct_vm,market.finalize_compile,key)
    assert not json.loads(market.get_market(key))['accepted']

@pytest.mark.parametrize('changes',[{'options':['YES','YES']},{'options':['YES']},{'article':'Evil participant source'},{'episode':2}])
def test_invalid_spec(market,direct_vm,changes):
    answer(direct_vm,**changes)
    with pytest.raises(Exception):market.propose('Does Alex survive?','Test Show',1,1)

def test_unauthorized_rehearsal(market,direct_vm,direct_bob):
    direct_vm.sender=direct_bob
    with direct_vm.expect_revert('owner-only'):market.rehearse('Does Alex survive?','Test Show',1,1)
