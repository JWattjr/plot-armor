"""Instrument a separate zero-value compiler diagnostic; never replace product contracts."""
import json
from chain import ROOT, client, transaction, save

p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
c=client()
source=(ROOT/'contracts/plot_markets.py').read_text(encoding='utf8')
source=source.replace("    require(type(answer) is dict and set(answer)==", "    print('COMPILE_MODEL_OUTPUT='+canonical(answer))\n    require(type(answer) is dict and set(answer)==",1)
(ROOT/'contracts/compile_diagnostic.py').write_text(source,encoding='utf8')
if not p.get('compileDiagnostic'):
    result=transaction(c,p,'deploy-compile-diagnostic',code=source)
    p['compileDiagnostic']=result.get('recipient',result.get('to_address'))
    save(p)
transaction(c,p,'diagnose-live-compile',p['compileDiagnostic'],'propose',['In War season 1 episode 4 (broadcast 2026-10-22T21:00:00-04:00), does Johnny Warren resign from Cathcarts? Answer YES or NO.','WAR',1,4])
