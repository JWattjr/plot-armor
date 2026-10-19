"""Instrument a separate zero-value compiler diagnostic; never replace product contracts."""
import json
from chain import ROOT, client, transaction, save

p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
c=client()
source=(ROOT/'contracts/compile_diagnostic.py').read_text(encoding='utf8')
# This frozen instrumented source reproduces the preceding compiler defect.
# It is intentionally separate from the repaired product implementation.
if not p.get('compileDiagnostic'):
    result=transaction(c,p,'deploy-compile-diagnostic',code=source)
    p['compileDiagnostic']=result.get('recipient',result.get('to_address'))
    save(p)
transaction(c,p,'diagnose-live-compile',p['compileDiagnostic'],'propose',['In War season 1 episode 4 (broadcast 2026-10-22T21:00:00-04:00), does Johnny Warren resign from Cathcarts? Answer YES or NO.','WAR',1,4])
