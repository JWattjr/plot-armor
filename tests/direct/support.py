import json,sys
from pathlib import Path
from datetime import datetime,timezone
T=2000000000
A='0x'+'11'*20
B='0x'+'22'*20
def warp(vm,t):
    vm.warp(datetime.fromtimestamp(t,timezone.utc).isoformat())
    sdk=sys.modules.get('genlayer.gl')
    if sdk is not None and getattr(sdk,'message_raw',None) is not None:sdk.message_raw['datetime']=vm._datetime
def helpers(file):
    scope={};s=Path(file).read_text(encoding='utf8');exec(compile(s.split('\n@gl.evm.contract_interface')[0].split('\nclass ')[0],file,'exec'),scope);return scope
def self_call(vm,fn,*args):
    old=vm.sender;vm.sender=vm._contract_address;fn(*args);vm.sender=old
def stub(monkeypatch,state):
    import genlayer.gl as sdk
    class Proxy:
        def view(self):return self
        def emit(self,**kwargs):return self
        def finalize_compile(self,*args):pass
        def finalize_resolution(self,*args):pass
        def finalize_pool(self,*args):pass
        def get_market(self,key):return json.dumps(state['market'])
        def get_resolution(self,key):return json.dumps(state.get('resolution',{}))
    monkeypatch.setattr(sdk,'get_contract_at',lambda _:Proxy())
def spec():return {'show':'Test Show','season':1,'episode':1,'title':'The Turn','air_utc':T+86400,'article':'Test Show (season 1)','extraction':'row','proposition':'Does Alex survive?','definitions':'Alive at the end; omission is UNCLEAR. Death must be explicit.','options':['YES','NO'],'rehearsal':False,'entry_deadline':T+100,'resolution_deadline':T+200}
