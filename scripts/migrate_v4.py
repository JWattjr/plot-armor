"""Start the repaired compiler release without authorizing any new GEN deposit."""
import copy
import json
import shutil
import subprocess
from chain import ROOT, save

p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
if p.get('releaseGeneration')==4:
    print('Generation 4 already initialized.');raise SystemExit(0)
assert p['poolDemo']['account']['claim']['status']=='PAID'
old=copy.deepcopy(p)
old.pop('previousReleases',None)
old['sourceCommit']='a6ade8d'+subprocess.check_output(['git','rev-parse','a6ade8d'],cwd=ROOT,text=True).strip()[7:]
archive=ROOT/'deploy/previous-v3-receipts'
assert not archive.exists(),'Archive exists; inspect before migrating'
shutil.copytree(ROOT/'deploy/receipts',archive)
p.setdefault('previousReleases',[]).append(old)
p['poolDemo']['legacyContracts']=copy.deepcopy(p['contracts'])
p['poolDemo']['sourceCommit']=old['sourceCommit']
native=['fund-demo','prepare-demo-stake','deposit-demo-11-wei','settle-demo-pool','settle-demo-pool-child-0','claim-demo-pool','claim-demo-pool-child-0','verify-demo-claim']
p['transactions']={'legacy-'+name:old['transactions'][name] for name in native}
p['contracts']={};p['markets']=[];p['failedTransactions']={}
p['releaseGeneration']=4;p['submissionReady']=False
p['sourceCommit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
p['blockers']=['Repaired compiler release is being deployed and rerun; the previous 11 wei demonstration remains PAID.','Exact 1440x960 browser checks and extension signing remain unverified.']
save(p)
print('Generation 4 initialized. Preserved PAID native demonstration; no new deposit will be made.')
