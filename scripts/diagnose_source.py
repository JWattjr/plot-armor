"""Zero-value diagnostic through the deployed Wikipedia access probe."""
import json
from urllib.parse import quote
from chain import ROOT, client, transaction, read, save

p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
c=client()
url='https://en.wikipedia.org/w/api.php?action=query&format=json&list=search&srlimit=5&srsearch='+quote('War (TV series) season 1 episodes',safe='')
transaction(c,p,'diagnose-wikipedia-search',p['probeContract'],'probe',[url])
result=read(c,p['probeContract'],'result',[url])
p.setdefault('probes',{})[url]=result
save(p)
print(json.dumps(result),flush=True)
