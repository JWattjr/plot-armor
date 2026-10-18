import json
from chain import ROOT,client,transaction,read,save
p=json.loads((ROOT/'deploy/proof.json').read_text())
c=client()
if not p.get('probeContract'):
    r=transaction(c,p,'deploy-probe',code=(ROOT/'contracts/access_probe.py').read_text())
    p['probeContract']=r.get('recipient',r.get('to_address'));save(p)
urls=['https://en.wikipedia.org/w/api.php?action=query&format=json&prop=revisions&titles=Ozymandias%20%28Breaking%20Bad%29&rvprop=ids%7Ctimestamp&rvdir=newer&rvstart=2013-09-18T01%3A00%3A00Z&rvlimit=1','https://en.wikipedia.org/w/index.php?title=Ozymandias_%28Breaking_Bad%29&oldid=1378002747&action=raw']
for i,url in enumerate(urls):
    transaction(c,p,'probe-'+str(i),p['probeContract'],'probe',[url])
    p.setdefault('probes',{})[url]=read(c,p['probeContract'],'result',[url]);save(p)
    print(json.dumps(p['probes'][url]),flush=True)
