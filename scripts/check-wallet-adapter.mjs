// Real signing through the app adapter, with a local Node EIP-1193 provider.
// This checks the transport and chain state, not a browser-extension popup.
import {existsSync,readFileSync,writeFileSync} from 'node:fs';
import {privateKeyToAccount} from 'viem/accounts';
import {send} from '../lib/wallet.ts';
const proof=JSON.parse(readFileSync('deploy/proof.json','utf8'));
const market=proof.markets.find(m=>m.accepted&&!m.spec.rehearsal);
if(!market)throw Error('A live finalized market is required');
const keys=JSON.parse(readFileSync('.secrets/demo-accounts.json','utf8'));
const account=privateKeyToAccount('0x'+keys[0].replace(/^0x/,''));
const file='deploy/wallet-adapter-check.json';
const old=existsSync(file)?JSON.parse(readFileSync(file,'utf8')):null;
const record=old?.contract===proof.contracts.PlotSeasons.address?old:{scope:'Real local Node signing through app EIP-1193 adapter; extension popup untested',contract:proof.contracts.PlotSeasons.address,marketId:market.id,account:account.address.toLowerCase(),valueWei:'0',hash:null,state:'NOT_SUBMITTED'};
const save=()=>writeFileSync(file,JSON.stringify(record,null,2));
const rpcURL='https://studio.genlayer.com/api';let last=0;
const original=globalThis.fetch;
globalThis.fetch=async(input,init)=>{const url=typeof input==='string'?input:input instanceof URL?input.href:input.url;if(url===rpcURL){await new Promise(r=>setTimeout(r,Math.max(0,2600-(Date.now()-last))));last=Date.now();const headers=new Headers(init?.headers);headers.set('User-Agent','Mozilla/5.0 PlotArmorWalletCheck/1.0');return original(input,{...init,headers})}return original(input,init)};
async function rpc(method,params=[]){const response=await fetch(rpcURL,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({jsonrpc:'2.0',id:1,method,params})});const r=await response.json();if(!response.ok||r.error)throw Error(r.error?.message??'RPC failed');return r.result}
Object.defineProperty(globalThis,'window',{value:{ethereum:{request:async({method,params=[]})=>{
 if(method==='eth_requestAccounts'||method==='eth_accounts')return [account.address];if(method==='eth_chainId')return '0xf22f';
 if(method==='eth_sendTransaction'){const tx=params[0];if(BigInt(tx.value??0)!==0n)throw Error('Only a zero-value free prediction is authorized by this script');const raw=await account.signTransaction({chainId:61999,type:'legacy',to:tx.to,data:tx.data,nonce:Number(BigInt(tx.nonce)),gas:BigInt(tx.gas),gasPrice:BigInt(tx.gasPrice),value:0n});return rpc('eth_sendRawTransaction',[raw])}
 return rpc(method,params);
}}}});
if(record.state==='FINALIZED_SUCCESS'){console.log(record.state,record.hash);process.exit(0)}
if(!record.hash){const result=await send(record.contract,'predict',[record.marketId,0],hash=>{record.hash=hash;record.state='SUBMITTED';save()});record.hash=result.hash;save()}
for(let i=0;i<180;i++){const r=await rpc('eth_getTransactionByHash',[record.hash]);if(r?.status==='FINALIZED'){record.state=r.consensus_data?.leader_receipt?.[0]?.execution_result==='SUCCESS'&&[undefined,'AGREE','MAJORITY_AGREE'].includes(r.result_name)?'FINALIZED_SUCCESS':'FINALIZED_ERROR';record.receipt=r;save();if(record.state!=='FINALIZED_SUCCESS')throw Error('Adapter execution failed');console.log(record.state,record.hash);process.exit(0)}if(i%6===0)console.log('Adapter waiting',r?.status??'submitted');await new Promise(r=>setTimeout(r,10000))}
throw Error('Pending hash retained; rerun to resume');
