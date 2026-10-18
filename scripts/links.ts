import {readFileSync} from 'node:fs';
import {explorer} from '../lib/explorer';
import type {Proof} from '../lib/domain';
const p=JSON.parse(readFileSync('deploy/proof.json','utf8')) as Proof;
console.log(JSON.stringify({contracts:Object.fromEntries(Object.entries(p.contracts).map(([name,c])=>[name,{page:explorer('address',c.address),api:explorer('addressApi',c.address)}])),transactions:Object.fromEntries(Object.entries(p.transactions).map(([name,h])=>[name,{page:explorer('tx',h),api:explorer('txApi',h)}]))}));
