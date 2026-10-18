import json,pytest
from support import *
from conftest import to_hex
@pytest.fixture
def seasons(direct_vm,direct_deploy,direct_owner,monkeypatch):
    direct_vm.sender=direct_owner;warp(direct_vm,T);c=direct_deploy('contracts/plot_seasons.py',A,B)
    state={'market':{'status':'OPEN','spec':spec()},'resolution':{'status':'RESOLVED','outcome':0}};stub(monkeypatch,state);return c,state

def test_points_streak_and_double_score(seasons,direct_vm):
    c,_=seasons;w=to_hex(direct_vm.sender);c.predict('m',0);c.score(w,'m');r=json.loads(c.leaderboard(''))[0];assert r['points']==10 and r['streak']==1
    with direct_vm.expect_revert('pending prediction'):c.score(w,'m')
    with direct_vm.expect_revert('prediction exists'):c.predict('m',1)

def test_rehearsal_excluded(seasons,direct_vm):
    c,state=seasons;state['market']['spec']['rehearsal']=True;c.predict('m',0);c.score(to_hex(direct_vm.sender),'m');assert json.loads(c.leaderboard(''))[0]['points']==0

def test_void_timeout_and_cutoff(seasons,direct_vm):
    c,state=seasons;w=to_hex(direct_vm.sender);c.predict('m',0);state['resolution']={};warp(direct_vm,T+200);c.score(w,'m');assert json.loads(c.get_predictions(w))[0]['status']=='VOID'
    with direct_vm.expect_revert('open finalized'):c.predict('late',0)

def test_scoring_order_cannot_improve_streak(seasons,direct_vm):
    c,state=seasons;w=to_hex(direct_vm.sender);c.predict('first',0);state['market']['spec']['air_utc']+=10;c.predict('second',0);c.score(w,'second');assert json.loads(c.leaderboard(''))[0]['streak']==1
    state['resolution']['outcome']=1;c.score(w,'first');assert json.loads(c.leaderboard(''))[0]['streak']==1

def test_terminal_resolution_scores_after_deadline(seasons,direct_vm):
    c,_=seasons;w=to_hex(direct_vm.sender);c.predict('m',0);warp(direct_vm,T+500);c.score(w,'m');assert json.loads(c.get_predictions(w))[0]['points']==10
