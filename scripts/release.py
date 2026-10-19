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
    markets=[]
    for key in keys:
        m=read(c,address('PlotMarkets'),'get_market',[key])
        if m.get('accepted') and 'PlotResolver' in p['contracts']:
            m['resolution']=read(c,address('PlotResolver'),'get_resolution',[key])
        if 'PlotPools' in p['contracts']:m['pool']=read(c,address('PlotPools'),'get_pool',[key])
        markets.append(m)
    p['markets']=markets
    p['recordedAt']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());save(p)
if stage=='deploy':
    for name,file in names.items():
        if name in p['contracts']:continue
        args=[] if name=='PlotMarkets' else [address('PlotMarkets')] if name=='PlotResolver' else [address('PlotMarkets'),address('PlotResolver')]
        code=(ROOT/'contracts'/file).read_text()
        receipt=transaction(c,p,'deploy-v'+str(p.get('releaseGeneration',4))+'-'+name,code=code,args=args)
        p['contracts'][name]={'address':receipt.get('recipient',receipt.get('to_address')),'source':file,'sourceSha256':hashlib.sha256(code.encode()).hexdigest()};save(p)
elif stage=='seed':
    cases=[('yes','In Ozymandias (broadcast 2013-09-15T21:00:00-04:00), does Hank Schrader die? Answer YES or NO.','Breaking Bad',5,14),('no','In Felina (broadcast 2013-09-29T21:00:00-04:00), does Jesse Pinkman die? Answer YES or NO.','Breaking Bad',5,16),('choice','In The Mountain and the Viper (broadcast 2014-06-01T21:00:00-04:00), who wins the trial by combat? Options: Oberyn Martell, Gregor Clegane.','Game of Thrones',4,8),('reject','Is this the best episode ever?','Breaking Bad',5,14)]
    for label,q,show,s,e in cases:
        name=adjudication_label(p,'compile-'+label)
        transaction(c,p,name,address('PlotMarkets'),'rehearse',[q,show,s,e]);record()
        if label=='yes' and not p.get('poolDemo') and (ROOT/'.secrets/deposit-approval.json').exists():
            from chain import signer,final
            approval=json.loads((ROOT/'.secrets/deposit-approval.json').read_text());assert approval['approvedDepositWei']=='11'
            funding=json.loads((ROOT/'deploy/funding.json').read_text());final(c,funding['hash'],'fund-demo')
            p['transactions']['fund-demo']=funding['hash']
            ids=read(c,address('PlotMarkets'),'get_ids');key=ids[0]
            p['poolDemo']={'marketId':key,'wallet':signer().address.lower(),'approvedDepositWei':'11','ticket':'ticket-1'};save(p)
            transaction(c,p,'prepare-demo-stake',address('PlotPools'),'prepare_stake',[key,0,11])
            t=read(c,address('PlotPools'),'get_ticket',['ticket-1']);assert t['market']==key and t['wallet']==signer().address.lower() and t['amount']==11
            transaction(c,p,'deposit-demo-11-wei',address('PlotPools'),'deposit',['ticket-1'],value=11);record()

elif stage=='reject':
    transaction(c,p,adjudication_label(p,'compile-reject'),address('PlotMarkets'),'rehearse',['Is this finale the best episode ever?','Severance (TV series)',2,10]);record()
elif stage=='live':
    for e,q in [(4,'In the upcoming episode Sing (broadcast 2026-10-22T21:00:00-04:00), does Johnny Warren die? Answer YES or NO.'),(5,'In the upcoming episode Every Little Thing She Does (broadcast 2026-10-29T21:00:00-04:00), do Morgan Henderson and Carla Duval sign a final divorce agreement? Answer YES or NO.')]:
        expected_air={4:1792717200,5:1793322000}[e]
        base='compile-live-upcoming-'+str(e)
        existing=[m for m in p['markets'] if m.get('spec') and not m['spec']['rehearsal'] and m['spec']['episode']==e and m['spec']['show'].casefold().startswith('war')]
        if existing:
            assert all(m['spec']['air_utc']==expected_air for m in existing),'Frozen live broadcast differs from the verified official schedule'
            if base in p['transactions']:transaction(c,p,base,address('PlotMarkets'),'propose',[q,'War (TV series)',1,e]);record()
            continue
        transaction(c,p,adjudication_label(p,base),address('PlotMarkets'),'propose',[q,'War (TV series)',1,e]);record()
        for market in p['markets']:
            spec=market.get('spec')
            if spec and not spec['rehearsal'] and spec['episode']==e:
                assert spec['air_utc']==expected_air,'Frozen live broadcast differs from the verified official schedule'
elif stage=='settle':
    record()
    for m in p['markets']:
        if m.get('status')!='OPEN' or time.time()<m['spec']['air_utc']+172800:continue
        old=m.get('resolution',{})
        if old.get('status') in ('RESOLVED','VOID'):continue
        label='resolve-'+m['id']+'-'+str(old.get('attempt',0)+1)
        transaction(c,p,adjudication_label(p,label),address('PlotResolver'),'resolve',[m['id']]);record()
        if int(m.get('pool',{}).get('total',0))>0 and m.get('pool',{}).get('status')=='OPEN' and time.time()>=m['spec']['entry_deadline']:
            transaction(c,p,'settle-pool-'+m['id'],address('PlotPools'),'settle',[m['id']]);record()
elif stage=='pool':
    if p.get('poolDemo',{}).get('account',{}).get('claim',{}).get('status')=='PAID':
        print('The approved 11 wei demonstration is already PAID; no new deposit is authorized.');raise SystemExit(0)
    approval=json.loads((ROOT/'.secrets/deposit-approval.json').read_text())
    assert approval['approvedDepositWei']=='11'
    funding=json.loads((ROOT/'deploy/funding.json').read_text())
    assert funding['wei']=='11'
    from chain import final,signer
    final(c,funding['hash'],'fund-demo')
    p['transactions']['fund-demo']=funding['hash'];save(p)
    if not p.get('poolDemo'):
        before=read(c,address('PlotMarkets'),'get_ids')
        transaction(c,p,adjudication_label(p,'compile-pool-demo'),address('PlotMarkets'),'rehearse',['In Ozymandias (broadcast 2013-09-15T21:00:00-04:00), does Hank Schrader die? Answer YES or NO.','Breaking Bad',5,14])
        ids=read(c,address('PlotMarkets'),'get_ids')
        created=[key for key in ids if key not in before]
        assert len(created)==1,'Ambiguous demo market; inspect before retrying'
        p['poolDemo']={'marketId':created[0],'wallet':signer().address.lower(),'approvedDepositWei':'11'};save(p)
    key=p['poolDemo']['marketId']
    transaction(c,p,'prepare-demo-stake',address('PlotPools'),'prepare_stake',[key,0,11])
    # Only this release account can create tickets in this isolated pool demo.
    ticket='ticket-1';t=read(c,address('PlotPools'),'get_ticket',[ticket])
    assert t['market']==key and t['wallet']==signer().address.lower() and t['amount']==11
    transaction(c,p,'deposit-demo-11-wei',address('PlotPools'),'deposit',[ticket],value=11)
    p['poolDemo']['ticket']=ticket;save(p);record()
elif stage=='claim':
    if p.get('poolDemo',{}).get('account',{}).get('claim',{}).get('status')=='PAID':
        print('The approved demonstration is already PAID. Original receipts are preserved.');raise SystemExit(0)
    from chain import signer
    key=p['poolDemo']['marketId']
    pool=read(c,address('PlotPools'),'get_pool',[key])
    if pool.get('status')!='SETTLED':transaction(c,p,'settle-demo-pool',address('PlotPools'),'settle',[key])
    transaction(c,p,'claim-demo-pool',address('PlotPools'),'claim',[key,1])
    parent=p['transactions']['claim-demo-pool'];child=p['transactions']['claim-demo-pool-child-0']
    transaction(c,p,'verify-demo-claim',address('PlotPools'),'verify_claim',[key,signer().address.lower(),1,parent,child])
    p['poolDemo']['account']=read(c,address('PlotPools'),'get_account',[key,signer().address.lower()]);save(p);record()
elif stage=='free':
    record()
    live=[m for m in p['markets'] if m.get('accepted') and not m['spec']['rehearsal']]
    if not live:
        # Demo dependency: seed the disambiguated live candidates first. The
        # parent does not write while its child runs, then reloads the journal.
        result=subprocess.run([sys.executable,'scripts/release.py','live'])
        assert result.returncode==0,'Live demo preparation failed; rerun to resume'
        p=json.loads((ROOT/'deploy/proof.json').read_text(encoding='utf8'))
        live=[m for m in p['markets'] if m.get('accepted') and not m['spec']['rehearsal']]
    assert live,'No live market'
    from chain import signer
    result=subprocess.run(['node','--import','tsx','scripts/check-wallet-adapter.mjs']);assert result.returncode==0,'Wallet adapter check failed'
    check=json.loads((ROOT/'deploy/wallet-adapter-check.json').read_text());p['transactions']['predict-live-free']=check['hash'];save(p)
    p['freeDemo']={'wallet':signer().address.lower(),'marketId':live[0]['id'],'predictions':read(c,address('PlotSeasons'),'get_predictions',[signer().address.lower()]),'leaderboard':read(c,address('PlotSeasons'),'leaderboard',[''])};save(p)
elif stage=='record':record()
else:raise SystemExit('Stages: deploy, seed, live, settle, record')
