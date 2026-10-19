import {readFileSync} from 'node:fs';
import {explorer} from '../lib/explorer';
import type {Proof} from '../lib/domain';
const p=JSON.parse(readFileSync(process.argv[2]??'deploy/proof.json','utf8')) as Proof&{poolDemo?:{legacyContracts?:Proof['contracts']}};
const contractLinks=(contracts:Proof['contracts'])=>Object.fromEntries(Object.entries(contracts).map(([name,c])=>[name,{page:explorer('address',c.address),api:explorer('addressApi',c.address)}]));
console.log(JSON.stringify({contracts:contractLinks(p.contracts),legacyContracts:contractLinks(p.poolDemo?.legacyContracts??{}),transactions:Object.fromEntries(Object.entries(p.transactions).map(([name,h])=>[name,{page:explorer('tx',h),api:explorer('txApi',h)}]))}));
