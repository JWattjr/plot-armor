# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""No LLM. Free predictions, immutable score order and per-season leaderboards."""
import json
from datetime import datetime
from genlayer import *

def now():
    return int(datetime.fromisoformat(str(gl.message_raw['datetime']).replace('Z','+00:00')).timestamp())

def require(ok,message):
    if not ok:
        raise gl.vm.UserError('[EXPECTED] '+message)

class PlotSeasons(gl.Contract):
    markets: Address
    resolver: Address
    predictions: TreeMap[str,str]
    users: DynArray[str]
    known: TreeMap[str,bool]

    def __init__(self,markets: str,resolver: str):
        self.markets=Address(markets);self.resolver=Address(resolver)

    @gl.public.write
    def predict(self,key: str,option: int) -> None:
        market=json.loads(gl.get_contract_at(self.markets).view().get_market(key))
        require(market.get('status')=='OPEN' and now()<market['spec']['entry_deadline'],'open finalized market required')
        spec=market['spec'];require(type(option) is int and 0<=option<len(spec['options']),'listed option required')
        wallet=str(gl.message.sender_address).lower()
        rows=json.loads(self.predictions.get(wallet,'[]'))
        require(len(rows)<200 and all(p['market']!=key for p in rows),'prediction exists or capacity reached')
        rows.append({'market':key,'option':option,'season':spec['show']+' / S'+str(spec['season']),'air_utc':spec['air_utc'],'deadline':spec['resolution_deadline'],'rehearsal':spec['rehearsal'],'status':'PENDING','points':0})
        self.predictions[wallet]=json.dumps(rows)
        if not self.known.get(wallet,False):
            require(len(self.users)<2000,'leaderboard capacity reached')
            self.known[wallet]=True;self.users.append(wallet)

    @gl.public.write
    def score(self,wallet: str,key: str) -> None:
        wallet=wallet.lower();rows=json.loads(self.predictions.get(wallet,'[]'))
        row=next((p for p in rows if p['market']==key),None)
        require(row is not None and row['status']=='PENDING','pending prediction required')
        # Finalized self callback in Resolver makes these terminal flags safe.
        result=json.loads(gl.get_contract_at(self.resolver).view().get_resolution(key))
        if result.get('status') not in ('RESOLVED','VOID') and now()>=row['deadline']:
            result={'status':'VOID'}
        require(result.get('status') in ('RESOLVED','VOID'),'result pending')
        row['status']='VOID' if result['status']=='VOID' else 'CORRECT' if result['outcome']==row['option'] else 'INCORRECT'
        row['points']=10 if row['status']=='CORRECT' and not row['rehearsal'] else 0
        self.predictions[wallet]=json.dumps(rows)

    @gl.public.view
    def get_predictions(self,wallet: str) -> str:
        return self.predictions.get(wallet.lower(),'[]')

    @gl.public.view
    def leaderboard(self,season: str) -> str:
        board=[]
        for wallet in self.users:
            rows=json.loads(self.predictions[wallet])
            rows=sorted([r for r in rows if not r['rehearsal'] and (not season or r['season']==season)],key=lambda r:(r['air_utc'],r['market']))
            points=0;streak=0;best=0;correct=0
            # Pending predictions break the observable streak, so scoring order
            # cannot manufacture a better streak by skipping a losing market.
            for row in rows:
                points+=row['points']
                if row['status']=='CORRECT':
                    streak+=1;correct+=1;best=max(best,streak)
                elif row['status']!='VOID':
                    streak=0
            board.append({'wallet':wallet,'points':points,'correct':correct,'streak':streak,'best_streak':best,'calls':len(rows)})
        return json.dumps(sorted(board,key=lambda r:(-r['points'],-r['best_streak'],r['wallet'])))
