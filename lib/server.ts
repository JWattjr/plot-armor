import 'server-only';
import fs from 'node:fs';
import path from 'node:path';
import {createClient,decodeLocalnetTransaction} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
import {TransactionHashVariant,type TransactionHash} from 'genlayer-js/types';
import type {Proof,Market} from './domain';
import {transactionState} from './domain';
// The browser reaches this server; upstream RPC gets the required browser UA.
const marker=Symbol.for('plot-armor.rpc-ua');
const state=globalThis as typeof globalThis&{[marker]?:boolean};
if(!state[marker]){const original=globalThis.fetch;globalThis.fetch=async(input,init)=>{const url=typeof input==='string'?input:input instanceof URL?String(input):input.url;if(url==='https://studio.genlayer.com/api'){const headers=new Headers(init?.headers);headers.set('User-Agent','Mozilla/5.0 PlotArmor/1.0');return original(input,{...init,headers})}return original(input,init)};state[marker]=true}
export function proof():Proof{return JSON.parse(fs.readFileSync(path.join(process.cwd(),'deploy/proof.json'),'utf8')) as Proof}
const client=createClient({chain:studionet,endpoint:'https://studio.genlayer.com/api'});
let history:number[]=[];
let tail=Promise.resolve();
const cache=new Map<string,{at:number;value:unknown}>();
const inflight=new Map<string,Promise<unknown>>();
async function limited<T>(key:string,fn:()=>Promise<T>,ttl=30000):Promise<T>{
 const old=cache.get(key);if(old&&Date.now()-old.at<ttl)return old.value as T;
 const active=inflight.get(key);if(active)return active as Promise<T>;
 const promise=(async()=>{const previous=tail;let release!:()=>void;tail=new Promise<void>(r=>{release=r});await previous;try{history=history.filter(t=>Date.now()-t<3600000);if(history.length>=440||history.filter(t=>Date.now()-t<60000).length>=24)throw Error('StudioNet read budget reached. Retry later.');history.push(Date.now());const value=await fn();cache.set(key,{at:Date.now(),value});return value}finally{await new Promise(r=>setTimeout(r,2200));release()}})().finally(()=>inflight.delete(key));inflight.set(key,promise);return promise;
}
const methods:Record<string,string[]>={PlotMarkets:['get_market','get_ids'],PlotResolver:['get_resolution'],PlotPools:['get_pool','get_ticket','get_account'],PlotSeasons:['get_predictions','leaderboard']};
export async function read<T>(contract:string,method:string,args:unknown[]=[]):Promise<T>{
 if(!methods[contract]?.includes(method)||args.length>2||args.some(a=>typeof a!=='string'||a.length>200))throw Error('Unsupported read');
 const address=proof().contracts[contract]?.address;if(!address)throw Error('Contract deployment is not recorded yet.');
 return limited(contract+method+JSON.stringify(args),async()=>{const v=await client.readContract({address:address as `0x${string}`,functionName:method,args:args as never[],transactionHashVariant:TransactionHashVariant.LATEST_FINAL});return (typeof v==='string'&&/^[\[{]/.test(v)?JSON.parse(v):v) as T});
}
export async function market(id:string):Promise<Market>{
 const m=await read<Market>('PlotMarkets','get_market',[id]);
 if(!m.id)throw Error('Market does not exist in finalized state.');
 if(m.accepted){m.resolution=await read('PlotResolver','get_resolution',[id]);m.pool=await read('PlotPools','get_pool',[id])}
 return m;
}
export async function transaction(hash:string){
 if(!/^0x[\da-f]{64}$/i.test(hash))throw Error('Invalid transaction hash');
 return limited('tx:'+hash,async()=>{
  const raw=await client.getTransaction({hash:hash as TransactionHash});if(!raw)return {hash,state:'SUBMITTED',appealDeadline:null,children:[]};
  const r=decodeLocalnetTransaction(raw as never) as unknown as Record<string,unknown>;
  const status=transactionState(r);let appealDeadline:number|null=null;
  if(status==='ACCEPTED'){
   const window=await client.request({method:'sim_getFinalityWindowTime' as never});
   const start=Number(r.timestamp_awaiting_finalization),processing=Number(r.appeal_processing_time??0),failed=Number(r.appeal_failed??0);
   if(r.leader_only===false&&r.appealed!==true&&start>0&&Number(window)>0)appealDeadline=start+processing+Number(window)*0.8**failed;
  }
  return {hash,state:status,appealDeadline,children:r.triggered_transactions??[],error:status==='FINALIZED_ERROR'?'Execution failed. No successful state change is recorded. Inspect the receipt.':null};
 },10000);
}
