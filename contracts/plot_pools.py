# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""No LLM. Integer parimutuel accounting, invalid-deposit credits and pull claims."""
import json
import base64
import re
from datetime import datetime
from genlayer.py import calldata
from genlayer import *

def now():
    return int(datetime.fromisoformat(str(gl.message_raw['datetime']).replace('Z','+00:00')).timestamp())

def require(ok,message):
    if not ok:
        raise gl.vm.UserError('[EXPECTED] '+message)

def allocation(pool):
    winner=pool['winner']
    if pool['status']=='VOID' or winner is None or pool['sides'][winner]==0:
        return {w:e['amount'] for w,e in pool['entries'].items()}
    result={}
    prefix=0
    for w,e in pool['entries'].items():
        if e['option']==winner:
            # Prefix allocation distributes every remainder wei deterministically.
            result[w]=pool['total']*(prefix+e['amount'])//pool['sides'][winner]-pool['total']*prefix//pool['sides'][winner]
            prefix+=e['amount']
        else:
            result[w]=0
    return result

def receipt(tx_hash):
    require(re.fullmatch(r'0x[0-9a-fA-F]{64}',tx_hash) is not None,'transaction hash required')
    response=gl.nondet.web.post('https://studio.genlayer.com/api',body=json.dumps({'jsonrpc':'2.0','id':1,'method':'eth_getTransactionByHash','params':[tx_hash]}).encode(),headers={'Content-Type':'application/json','User-Agent':'Mozilla/5.0 PlotArmor/1.0'})
    require(response.status==200,'receipt unavailable; retry')
    data=json.loads(response.body.decode())
    require(not data.get('error') and type(data.get('result')) is dict,'receipt unavailable; retry')
    return data['result']

def transfer_result(parent,child,contract,wallet,key,attempt,amount):
    require(parent.get('status')=='FINALIZED' and child.get('status')=='FINALIZED','transfer pending; retry verification')
    require(str(parent.get('to_address','')).lower()==contract and str(parent.get('from_address','')).lower()==wallet,'wrong claim parent')
    leader=(parent.get('consensus_data') or {}).get('leader_receipt') or [{}]
    require(leader[0].get('execution_result')=='SUCCESS','claim parent failed')
    encoded=parent.get('data',{}).get('calldata')
    require(type(encoded) is str,'parent calldata unavailable')
    call=calldata.decode(base64.b64decode(encoded))
    require(call=={'method':'claim','args':[key,attempt]},'wrong claim key or attempt')
    require(child.get('hash') in parent.get('triggered_transactions',[]) and child.get('triggered_by')==parent.get('hash'),'unrelated native child')
    require(str(child.get('from_address','')).lower()==contract and str(child.get('to_address','')).lower()==wallet and int(child.get('value',0))==amount,'wrong native transfer')
    require(child.get('type')==0 and child.get('consensus_data') is None and child.get('triggered_on')=='finalized','not a native finality transfer')
    require(type(child.get('value_credited')) is bool,'credit unknown; retry verification')
    return child['value_credited']

@gl.evm.contract_interface
class Recipient:
    class View:
        pass
    class Write:
        pass

class PlotPools(gl.Contract):
    markets: Address
    resolver: Address
    records: TreeMap[str,str]
    tickets: TreeMap[str,str]
    credits: TreeMap[str,u256]
    claims: TreeMap[str,str]
    recovered: TreeMap[str,bool]
    counter: u256

    def __init__(self,markets: str,resolver: str):
        require(int(gl.message.chain_id)==61999,'StudioNet simulated GEN only')
        self.markets=Address(markets);self.resolver=Address(resolver)
        self.counter=u256(0)

    @gl.public.write
    def prepare_stake(self,key: str,option: int,amount: int) -> str:
        market=json.loads(gl.get_contract_at(self.markets).view().get_market(key))
        require(market.get('status')=='OPEN','finalized open market required')
        spec=market['spec']
        require(now()<spec['entry_deadline'],'entries closed')
        require(type(option) is int and 0<=option<len(spec['options']) and 0<amount<=100*10**18,'invalid stake')
        wallet=str(gl.message.sender_address).lower()
        require(not spec['rehearsal'] or wallet==market['creator'],'historical pool is an owner-only rehearsal')
        r=json.loads(self.records.get(key,'{}'))
        if not r:
            r={'id':key,'status':'OPEN','spec_hash':market['spec_hash'],'deadline':spec['resolution_deadline'],'entry_deadline':spec['entry_deadline'],'sides':[0]*len(spec['options']),'total':0,'entries':{},'winner':None,'payouts':{},'mode':'REHEARSAL' if spec['rehearsal'] else 'LIVE'}
        require(r['status']=='OPEN' and wallet not in r['entries'] and len(r['entries'])<200,'one entry per wallet; pool full or closed')
        self.records[key]=json.dumps(r)
        self.counter=u256(int(self.counter)+1)
        ticket='ticket-'+str(self.counter)
        self.tickets[ticket]=json.dumps({'market':key,'wallet':wallet,'option':option,'amount':amount,'expires':min(now()+300,spec['entry_deadline']),'used':False})
        return ticket

    @gl.public.write.payable
    def deposit(self,ticket: str) -> str:
        # Never throw for a well-formed payable invocation. Failed validation
        # becomes an explicit refundable credit instead of untracked GEN.
        wallet=str(gl.message.sender_address).lower()
        amount=int(gl.message.value)
        t=json.loads(self.tickets.get(ticket,'{}'))
        r=json.loads(self.records.get(t.get('market',''),'{}'))
        valid=bool(t and r and t['wallet']==wallet and not t['used'] and amount==t['amount'] and now()<t['expires'] and r['status']=='OPEN' and wallet not in r['entries'])
        if not valid:
            self.credits[wallet]=u256(int(self.credits.get(wallet,u256(0)))+amount)
            return 'REFUND_CREDIT'
        t['used']=True
        r['entries'][wallet]={'option':t['option'],'amount':amount}
        r['sides'][t['option']]+=amount;r['total']+=amount
        self.records[t['market']]=json.dumps(r);self.tickets[ticket]=json.dumps(t)
        return 'STAKED'

    @gl.public.write
    def recover_failed_deposit(self,tx_hash: str) -> None:
        require(not self.recovered.get(tx_hash,False),'receipt already recovered')
        wallet=str(gl.message.sender_address).lower();contract=str(gl.message.contract_address).lower()
        def verify():
            r=receipt(tx_hash)
            require(r.get('status')=='FINALIZED' and r.get('value_credited') is True,'not finalized credited value')
            require(str(r.get('from_address','')).lower()==wallet and str(r.get('to_address','')).lower()==contract,'wrong deposit sender or recipient')
            leader=(r.get('consensus_data') or {}).get('leader_receipt') or [{}]
            require(leader[0].get('execution_result') not in (None,'SUCCESS'),'only failed execution can be recovered')
            value=int(r.get('value',0));require(value>0,'no deposit value')
            return value
        amount=gl.eq_principle.strict_eq(verify)
        self.recovered[tx_hash]=True
        self.credits[wallet]=u256(int(self.credits.get(wallet,u256(0)))+amount)

    @gl.public.write
    def settle(self,key: str) -> None:
        r=json.loads(self.records.get(key,'{}'));require(r and r['status']=='OPEN','open pool required')
        require(now()>=r['entry_deadline'],'entries still open')
        # Timeout is independent of resolver availability.
        if now()>=r['deadline']:
            r['status']='VOID'
        else:
            result=json.loads(gl.get_contract_at(self.resolver).view().get_resolution(key))
            require(result.get('spec_hash')==r['spec_hash'],'resolution does not match frozen spec')
            require(result.get('status') in ('RESOLVED','VOID'),'result pending; refund at deadline')
            r['status']=result['status'];r['winner']=result.get('outcome') if result['status']=='RESOLVED' else None
        r['payouts']=allocation(r);r['status']='SETTLING'
        self.records[key]=json.dumps(r)
        gl.get_contract_at(gl.message.contract_address).emit(on='finalized').finalize_pool(key)

    @gl.public.write
    def finalize_pool(self,key: str) -> None:
        require(gl.message.sender_address==gl.message.contract_address,'self finality callback only')
        r=json.loads(self.records[key])
        if r['status']=='SETTLING':
            r['status']='SETTLED';self.records[key]=json.dumps(r)

    @gl.public.write
    def claim(self,key: str,attempt: int) -> None:
        wallet=str(gl.message.sender_address).lower()
        claim_key=key+':'+wallet
        previous=json.loads(self.claims.get(claim_key,'{}'))
        new_credit=key=='credits' and int(self.credits.get(wallet,u256(0)))>0 and previous.get('status')=='PAID'
        require(not previous or previous['status']=='FAILED' or new_credit,'claim already paid or transfer pending')
        require(attempt==(previous['attempt']+1 if previous else 1),'wrong attempt')
        if previous and previous['status']=='FAILED':
            amount=previous['amount']
        elif key=='credits':
            amount=int(self.credits.get(wallet,u256(0)))
            self.credits[wallet]=u256(0)
        else:
            r=json.loads(self.records.get(key,'{}'))
            require(r.get('status')=='SETTLED','pool not finalized')
            amount=r['payouts'].get(wallet,0)
        require(amount>0 and int(self.balance)>=amount,'no claim or insufficient native balance')
        self.claims[claim_key]=json.dumps({'status':'PENDING','attempt':attempt,'amount':amount,'requested_at':now()})
        Recipient(Address(wallet)).emit_transfer(value=u256(amount),on='finalized')

    @gl.public.write
    def verify_claim(self,key: str,wallet: str,attempt: int,parent_hash: str,child_hash: str) -> None:
        wallet=wallet.lower();claim_key=key+':'+wallet
        c=json.loads(self.claims.get(claim_key,'{}'))
        require(c.get('status')=='PENDING' and c['attempt']==attempt,'matching pending claim required')
        contract=str(gl.message.contract_address).lower()
        def verify():
            return transfer_result(receipt(parent_hash),receipt(child_hash),contract,wallet,key,attempt,c['amount'])
        paid=gl.eq_principle.strict_eq(verify)
        c.update({'status':'PAID' if paid else 'FAILED','parent':parent_hash,'child':child_hash})
        self.claims[claim_key]=json.dumps(c)

    @gl.public.view
    def get_pool(self,key: str) -> str:
        return self.records.get(key,'{}')

    @gl.public.view
    def get_ticket(self,key: str) -> str:
        return self.tickets.get(key,'{}')

    @gl.public.view
    def get_account(self,key: str,wallet: str) -> str:
        wallet=wallet.lower()
        return json.dumps({'credit':str(self.credits.get(wallet,u256(0))),'claim':json.loads(self.claims.get(key+':'+wallet,'{}'))})
