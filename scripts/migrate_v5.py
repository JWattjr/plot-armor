"""Initialize metadata-only compilation, preserving the already-paid v3 pool."""
import copy,json,shutil,subprocess
from chain import ROOT,save

p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
if p.get('releaseGeneration')==5:
    print('Generation 5 already initialized.');raise SystemExit(0)
assert p.get('releaseGeneration')==4 and p['poolDemo']['account']['claim']['status']=='PAID'
assert p['poolDemo'].get('legacyContracts'),'Preserve the actual paid pool, not the empty replacement'
old=copy.deepcopy(p);old.pop('previousReleases',None)
old['sourceCommit']=subprocess.check_output(['git','rev-parse','defa973'],cwd=ROOT,text=True).strip()
archive=ROOT/'deploy/previous-v4-receipts'
assert not archive.exists(),'Archive exists; inspect before migrating'
shutil.copytree(ROOT/'deploy/receipts',archive)
p.setdefault('previousReleases',[]).append(old)
p['transactions']={name:h for name,h in p['transactions'].items() if name.startswith('legacy-')}
assert len(p['transactions'])==8,'All original approved native receipts must remain'
p['contracts']={};p['markets']=[];p['failedTransactions']={};p['releaseGeneration']=5
p['sourceCommit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
p['submissionReady']=False
p['blockers']=['Metadata-only compiler release is being proved on unaired and historical episodes. The original 11 wei demo remains PAID.','Exact 1440x960 browser checks and extension popup signing remain unverified.']
save(p)
print('Generation 5 initialized. Paid pool and all eight native receipts preserved; no deposit will be repeated.')
