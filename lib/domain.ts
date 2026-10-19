export type Spec = {show:string;season:number;episode:number;title:string;air_utc:number;article:string;extraction:string;proposition:string;definitions:string;options:string[];rehearsal:boolean;entry_deadline:number;resolution_deadline:number;source_revision?:number;source_digest?:string};
export type Resolution = {status?:string;outcome?:number|'UNCLEAR';quote?:string;url?:string;revision?:number;digest?:string;reason?:string;attempt?:number};
export type Pool = {status?:string;total?:number|string;sides?:(number|string)[];entries?:Record<string,{amount:number|string;option:number}>;payouts?:Record<string,number|string>;deadline?:number};
export type Market = {id:string;creator:string;question:string;status:string;accepted:boolean;reason:string;spec:Spec|null;spec_hash:string;created_at:number;resolution?:Resolution;pool?:Pool};
export type NativeDemo = {wei:string;pool:string;wallet:string;marketId?:string;status:string;parent?:string;child?:string;archived:boolean};
export function nativeAmount(wei:string):string {
  const value=BigInt(wei),unit=10n**18n;
  if(value<unit)return `${value} wei`;
  const fraction=(value%unit).toString().padStart(18,'0').replace(/0+$/,'');
  return `${value/unit}${fraction?'.'+fraction:''} GEN`;
}
export type Proof = {contracts:Record<string,{address:string;source:string;sourceSha256:string}>;transactions:Record<string,string>;markets:Market[];recordedAt?:string;website?:string;github?:string;sourceCommit?:string;submissionReady:boolean;blockers:string[];nativeDemo?:NativeDemo};
export type TxState = 'SUBMITTED'|'PENDING'|'ACCEPTED'|'FINALIZED_SUCCESS'|'FINALIZED_ERROR';
export function needsTransactionPolling(t:{state:TxState;readback?:unknown}):boolean {
  return !t.state.startsWith('FINALIZED')||(t.state==='FINALIZED_SUCCESS'&&t.readback===undefined);
}
export function transactionState(r:Record<string,unknown>):TxState {
  const status=r.status_name??r.statusName??r.status;
  if(status==='FINALIZED'||status===7){
    const data=r.consensus_data as {leader_receipt?:{execution_result?:string}[]}|undefined;
    const execution=r.txExecutionResultName??data?.leader_receipt?.[0]?.execution_result;
    const consensus=r.result_name??r.resultName;
    const agreed=consensus===undefined?(r.result===undefined||r.result===6||r.result==='6'):['AGREE','MAJORITY_AGREE','SUCCESS'].includes(String(consensus));
    return agreed&&['SUCCESS','FINISHED_WITH_RETURN'].includes(String(execution))?'FINALIZED_SUCCESS':'FINALIZED_ERROR';
  }
  if(status==='ACCEPTED'||status===6)return 'ACCEPTED';
  return !r.hash?'SUBMITTED':'PENDING';
}
export function shield(m:Market):Market {
  const r=m.resolution;
  return {...m,spec:m.spec?.rehearsal?{...m.spec,proposition:'Historical proposition hidden until result reveal.',definitions:'Historical definitions hidden until result reveal.'}:m.spec,reason:m.accepted?'Frozen specification accepted by validators.':m.reason,pool:m.pool?{status:m.pool.status,total:m.pool.total,sides:m.pool.sides,deadline:m.pool.deadline}:undefined,resolution:r?{status:r.status,attempt:r.attempt}:undefined};
}
export function publicProof(p:Proof&{poolDemo?:{approvedDepositWei:string;wallet:string;marketId?:string;legacyContracts?:Proof['contracts'];account?:{claim?:{status?:string;parent?:string;child?:string}}}}):Proof{
  // Whitelist fields: raw probe samples and previous releases can themselves
  // contain plot details, even when the current markets have been shielded.
  const demo=p.poolDemo;const pool=(demo?.legacyContracts??p.contracts).PlotPools?.address;const claim=demo?.account?.claim;
  const nativeDemo=demo&&pool?{wei:demo.approvedDepositWei,pool,wallet:demo.wallet,marketId:demo.marketId,status:claim?.status??'PENDING',parent:claim?.parent,child:claim?.child,archived:!!demo.legacyContracts}:undefined;
  return {contracts:p.contracts,transactions:p.transactions,markets:p.markets.map(shield),recordedAt:p.recordedAt,website:p.website,github:p.github,sourceCommit:p.sourceCommit,submissionReady:p.submissionReady,blockers:p.blockers,nativeDemo};
}
export function utc(seconds:number){return new Date(seconds*1000).toLocaleString('en-GB',{timeZone:'UTC',day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'})+' UTC'}
export function closed(m:Market,stamp=Date.now()/1000){return m.status!=='OPEN'||!m.spec||stamp>=m.spec.entry_deadline}
