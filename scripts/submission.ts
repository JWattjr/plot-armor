import {readFileSync,writeFileSync} from 'node:fs';
import {explorer} from '../lib/explorer';
import {wikipediaRevision} from '../lib/evidence';
import type {Proof} from '../lib/domain';
type Demo={marketId:string;wallet:string;approvedDepositWei:string;legacyContracts?:Proof['contracts'];account?:{claim?:{status?:string}};balances?:Record<string,{walletWei:string;poolWei:string;walletGEN:string;poolGEN:string;at:string}>;verifyCallback?:string};
const p=JSON.parse(readFileSync('deploy/proof.json','utf8')) as Proof&{poolDemo?:Demo;previousPoolDemos?:Demo[]};
const github=p.github??'https://github.com/JWattjr/plot-armor';
const demo=p.poolDemo;
if(!demo||demo.legacyContracts||demo.approvedDepositWei!=='2000000000000000000'||demo.account?.claim?.status!=='PAID')throw Error('Refusing to claim a 2 GEN payout before submitted PlotPools is verified PAID.');
const fields={
 contributionType:'Projects',projectName:'Plot Armor',primaryTag:'Gaming',tag1:'Outcome Verification',tag2:'Prediction Markets',
 oneLiner:'Bet on your favourite shows. GenLayer validators read the episode and settle it — spoiler-free.',
 description:'Plot Armor lets friends predict TV episode plots with spoiler-safe results. PlotMarkets compiles one objective question into frozen rules or rejects it. PlotResolver selects a permanent Wikipedia revision in code, extracts the episode summary, and asks validators for an outcome and a verbatim quote. Agreement covers the evidence digest, outcome and quote. PlotPools owns simulated GEN stakes, refunds and pull claims without an LLM. A 2 GEN payout is proven on the submitted PlotPools, including finalized native credit and exact wallet/pool balance reconciliation. PlotSeasons handles free predictions, points and streaks. Historical rehearsals are owner-only for stakes and excluded from competitive scoring. VOID/refund remains test-only; no natural VOID was manufactured. Source, receipts and resumable verification scripts are public.',
 howTo:[
  {heading:'Browse without a wallet',instruction:'Inspect upcoming episodes and settlement dates. Historical results stay shielded until you reveal them.'},
  {heading:'Inspect immutable evidence',instruction:'Reveal a historical result and follow its exact Wikipedia oldid and finalized receipt.'},
  {heading:'Propose and predict',instruction:'Connect a StudioNet wallet. Propose an objective unaired episode question or make a free prediction. Inspect the compiled rules or rejection after finality.'},
  {heading:'Inspect the submitted-pool payout',instruction:`Open market ${demo.marketId} or Proof. Inspect the 2 GEN PAID claim, native transfer, balances and finality receipts on the submitted PlotPools. The old 11 wei example is previous-deployment history.`},
  {heading:'Verify the release',instruction:'Run npm run verify for finalized receipts, submitted-pool paid state, exact balances and all documentation links. Use npm run settle only when live markets become eligible.'}
 ],
 expectedOutcome:'A question becomes frozen rules or a rejection. Validators resolve supported outcomes from permanent Wikipedia evidence. The submitted PlotPools has a proven 2 GEN payout with verified native credit and exact balances. VOID/refund is test-only because no natural VOID occurred. Upcoming War settlements remain pending until 25 October and 1 November 2026. Results stay shielded until reveal.',
 contractLinks:Object.values(p.contracts).map(c=>explorer('address',c.address)),website:p.website,github,
 evidence:['deploy/proof.json','docs/VERIFICATION.md','docs/TUTORIAL.md','docs/RELEASE_REPORT.md'].map(file=>`${github}/blob/main/${file}`)
};
const lengths={oneLiner:fields.oneLiner.length,description:fields.description.length,expectedOutcome:fields.expectedOutcome.length};
if(lengths.oneLiner>180||lengths.description>1000||lengths.expectedOutcome>500)throw Error('Portal text exceeds its limit');
writeFileSync('docs/submission/portal-fields.json',JSON.stringify(fields,null,2)+'\n');
console.log('Portal field lengths:',JSON.stringify(lengths));
const lines=['# Plot Armor release report','',`Website: [Plot Armor](${p.website}). Repository: [JWattjr/plot-armor](${github}).`,`Contract source commit: ${p.sourceCommit}. Recorded market snapshot: ${p.recordedAt}.`,'','## Submitted contracts','',...Object.entries(p.contracts).map(([name,c])=>`- [${name}](${explorer('address',c.address)}) — ${c.address}`),'','## Markets',''];
for(const m of p.markets){
 if(!m.accepted){lines.push(`- ${m.id}: ${m.status}. ${m.reason}`);continue}
 const r=m.resolution;const option=typeof r?.outcome==='number'?m.spec?.options[r.outcome]:r?.outcome??'pending';
 lines.push(`- ${m.id}: ${m.spec?.show}, S${m.spec?.season} E${m.spec?.episode}, ${m.spec?.title}. ${m.spec?.rehearsal?'Historical rehearsal':'Live forecast'}. Resolution: ${r?.status??'not requested'}; outcome: ${option}.`);
 if(m.spec&&!m.spec.rehearsal)lines.push(`  Upcoming live settlement eligibility: ${new Date((m.spec.air_utc+172800)*1000).toISOString()}; refund deadline: ${new Date(m.spec.resolution_deadline*1000).toISOString()}.`);
 if(m.spec?.source_revision)lines.push(`  Compiler metadata: [revision ${m.spec.source_revision}](${wikipediaRevision(m.spec.article,m.spec.source_revision)}).`);
 if(r?.url)lines.push(`  Evidence: [Wikipedia revision ${r.revision}](${r.url}).`);
}
lines.push('','## Proven payout on submitted PlotPools','',`Owner-approved stake and payout: **2 simulated GEN** (2000000000000000000 wei). Market: ${demo.marketId}. Wallet: ${demo.wallet}. Final claim status: **PAID**.`,`Pool: [${p.contracts.PlotPools.address}](${explorer('address',p.contracts.PlotPools.address)}).`,demo.verifyCallback??'verify_claim records verified native credit.','','| Finalized stage | Wallet (GEN) | PlotPools (GEN) | Wallet (wei) | PlotPools (wei) |','|---|---:|---:|---:|---:|');
for(const [stage,b] of Object.entries(demo.balances??{}))lines.push(`| ${stage} | ${b.walletGEN} | ${b.poolGEN} | ${b.walletWei} | ${b.poolWei} |`);
lines.push('','Wallet decrease on deposit and increase on native payout are exactly 2 GEN. The submitted pool returns to its initial native balance.','', '## New finalized receipts','');
for(const [name,hash] of Object.entries(p.transactions).filter(([name])=>name.startsWith('submitted-2gen-')))lines.push(`- [${name}](${explorer('tx',hash)})`);
lines.push('','## Previous-deployment history','');
for(const old of p.previousPoolDemos??[])if(old.legacyContracts)lines.push(`The 11 wei PAID example belongs to previous [pool ${old.legacyContracts.PlotPools.address}](${explorer('address',old.legacyContracts.PlotPools.address)}). It is historical evidence and is not the submitted-pool payout.`);
lines.push('','## Other recorded receipts','');
for(const [name,hash] of Object.entries(p.transactions).filter(([name])=>!name.startsWith('submitted-2gen-')))lines.push(`- [${name}](${explorer('tx',hash)})`);
lines.push('','## Honest limits','', 'VOID/refund is test-only: no natural VOID was manufactured. War live settlements are upcoming on 25 October and 1 November 2026 at 01:00 UTC. No contract was changed or redeployed. The Portal draft has not been submitted.','','## Release status','',p.submissionReady?'Required release proof is verified.':'Not marked submission-ready. See verification results and blockers.','',...p.blockers.map(b=>`- ${b}`),'',`Portal field lengths: ${JSON.stringify(lengths)}.`);
writeFileSync('docs/RELEASE_REPORT.md',lines.join('\n')+'\n');
