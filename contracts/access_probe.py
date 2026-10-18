# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
import json
import hashlib
from genlayer import *
class AccessProbe(gl.Contract):
    records: TreeMap[str,str]
    def __init__(self):
        pass
    @gl.public.write
    def probe(self, url: str) -> None:
        if not url.startswith('https://en.wikipedia.org/'):
            raise gl.vm.UserError('Wikipedia only')
        def fetch():
            try:
                r=gl.nondet.web.get(url,headers={'User-Agent':'Mozilla/5.0 PlotArmor/1.0'})
                s=r.body.decode('utf8',errors='replace')
                return {'status':r.status,'length':len(s),'digest':hashlib.sha256(s.encode()).hexdigest(),'sample':s[:500]}
            except Exception as e:
                return {'status':0,'length':0,'digest':'','sample':str(e)[:300]}
        def validate(result):
            own=fetch()
            return isinstance(result,gl.vm.Return) and own['status']==result.calldata['status'] and (own['length']>100)==(result.calldata['length']>100)
        self.records[url]=json.dumps(gl.vm.run_nondet_unsafe(fetch,validate))
    @gl.public.view
    def result(self,url: str) -> str:
        return self.records.get(url,'{}')
