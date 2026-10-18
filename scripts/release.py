"""Resumable stages. Never deposits GEN without --approved-deposit-wei."""
import json,sys,hashlib,subprocess,time
from chain import ROOT,client,transaction,read,save,adjudication_label
p=json.loads((ROOT/'deploy/proof.json').read_text());c=client()
stage=sys.argv[1] if len(sys.argv)>1 else 'record'
names={'PlotMarkets':'plot_markets.py','PlotResolver':'plot_resolver.py','PlotPools':'plot_pools.py','PlotSeasons':'plot_seasons.py'}
def address(name):return p['contracts'][name]['address']
def record():
    if 'PlotMarkets' not in p['contracts']:return
    keys=read(c,address('PlotMarkets'),'get_ids')
    p['markets']=[]
    for key in keys:
        m=read(c,address('PlotMarkets'),'get_market',[key])
        if m.get('accepted') and 'PlotResolver' in p['contracts']:
            m['resolution']=read(c,address('PlotResolver'),'get_resolution',[key])
        if 'PlotPools' in p['contracts']:m['pool']=read(c,address('PlotPools'),'get_pool',[key])
        p['markets'].append(m);save(p)
    p['recordedAt']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());save(p)
if stage=='deploy':
    for name,file in names.items():
        if name in p['contracts']:continue
        args=[] if name=='PlotMarkets' else [address('PlotMarkets')] if name=='PlotResolver' else [address('PlotMarkets'),address('PlotResolver')]
        code=(ROOT/'contracts'/file).read_text()
        receipt=transaction(c,p,'deploy-v2-'+name,code=code,args=args)
        p['contracts'][name]={'address':receipt.get('recipient',receipt.get('to_address')),'source':file,'sourceSha256':hashlib.sha256(code.encode()).hexdigest()};save(p)
elif stage=='seed':
    cases=[('yes','Does Hank Schrader die in this episode? Answer YES or NO.','Breaking Bad',5,14),('no','Does Jesse Pinkman die in this episode? Answer YES or NO.','Breaking Bad',5,16),('choice','Who wins the trial by combat between Oberyn Martell and Gregor Clegane? Options: Oberyn Martell, Gregor Clegane.','Game of Thrones',4,8),('reject','Is this the best episode ever?','Breaking Bad',5,14)]
    for label,q,show,s,e in cases:
        name=adjudication_label(p,'compile-'+label)
        transaction(c,p,name,address('PlotMarkets'),'rehearse',[q,show,s,e]);record()
elif stage=='live':
    for e,q in [(4,'Does Johnny Warren explicitly resign from Cathcarts during this episode? Answer YES or NO.'),(5,'Do Morgan Henderson and Carla Duval explicitly sign a final divorce agreement in this episode? Answer YES or NO.')]:
        transaction(c,p,adjudication_label(p,'compile-live-'+str(e)),address('PlotMarkets'),'propose',[q,'War',1,e]);record()
elif stage=='settle':
    record()
    for m in p['markets']:
        if m.get('status')!='OPEN' or time.time()<m['spec']['air_utc']+172800:continue
        old=m.get('resolution',{})
        if old.get('status') in ('RESOLVED','VOID'):continue
        label='resolve-'+m['id']+'-'+str(old.get('attempt',0)+1)
        transaction(c,p,adjudication_label(p,label),address('PlotResolver'),'resolve',[m['id']]);record()
        if m.get('pool',{}).get('status')=='OPEN' and time.time()>=m['spec']['entry_deadline']:
            transaction(c,p,'settle-pool-'+m['id'],address('PlotPools'),'settle',[m['id']]);record()
elif stage=='record':record()
else:raise SystemExit('Stages: deploy, seed, live, settle, record')
