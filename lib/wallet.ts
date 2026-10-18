import {createClient} from 'genlayer-js';
import {studionet} from 'genlayer-js/chains';
type Provider={request:(args:{method:string;params?:unknown[]})=>Promise<unknown>;on?:(event:string,listener:(...args:unknown[])=>void)=>void;removeListener?:(event:string,listener:(...args:unknown[])=>void)=>void};
declare global{interface Window{ethereum?:Provider}}
export async function wallet(onSent:(hash:string)=>void){
 const p=window.ethereum;if(!p)throw Error('Install a compatible wallet such as MetaMask to make a prediction. Browsing needs no wallet.');
 const accounts=await p.request({method:'eth_requestAccounts'}) as string[];if(!accounts[0])throw Error('Select an account.');
 if(await p.request({method:'eth_chainId'})!=='0xf22f'){try{await p.request({method:'wallet_switchEthereumChain',params:[{chainId:'0xf22f'}]})}catch(e){if((e as {code?:number}).code!==4902)throw e;await p.request({method:'wallet_addEthereumChain',params:[{chainId:'0xf22f',chainName:'GenLayer StudioNet',nativeCurrency:{name:'GEN',symbol:'GEN',decimals:18},rpcUrls:['https://studio.genlayer.com/api'],blockExplorerUrls:['https://explorer-studio.genlayer.com']}]})}}
 const provider:Provider={request:async a=>{if(a.method==='eth_sendTransaction'){const tx=a.params?.[0] as Record<string,unknown>;const hash=await p.request({...a,params:[{...tx,chainId:'0xf22f',type:'0x0',gasPrice:'0x0',value:tx.value??'0x0'}]});if(typeof hash==='string')onSent(hash);return hash}return p.request(a)}};
 return {account:accounts[0].toLowerCase(),client:createClient({chain:studionet,account:accounts[0] as `0x${string}`,provider})};
}
export async function send(contract:string,method:string,args:unknown[],onSent:(hash:string)=>void,value=0n){
 const {client,account}=await wallet(onSent);
 // Pinned 1.1.8 uses the legacy StudioNet ABI, without a protocol fees argument.
 // The provider sets explicit gasPrice=0; no estimated fee is silently added.
 const hash=await client.writeContract({address:contract as `0x${string}`,functionName:method,args:args as never[],value});
 return {hash:String(hash),account};
}
