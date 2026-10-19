import test from 'node:test';
import assert from 'node:assert/strict';
import {shield,transactionState,closed,type Market} from '../lib/domain';
import {explorer} from '../lib/explorer';
test('initial data cannot contain result or quote',()=>{const m={id:'market-1',resolution:{status:'RESOLVED',outcome:0,quote:'The hidden result',url:'https://en.wikipedia.org/?oldid=1',digest:'abc'},pool:{total:11,sides:[11,0],payouts:{viewer:11},entries:{viewer:{amount:11,option:0}}}} as unknown as Market;const serialized=JSON.stringify(shield(m));for(const value of ['outcome','quote','payouts','The hidden result'])assert.ok(!serialized.includes(value));});
test('finality alone is not execution success',()=>{assert.equal(transactionState({status:'FINALIZED',consensus_data:{leader_receipt:[{execution_result:'ERROR'}]}}),'FINALIZED_ERROR');assert.equal(transactionState({status:'FINALIZED',consensus_data:{leader_receipt:[{execution_result:'SUCCESS'}]}}),'FINALIZED_SUCCESS');assert.equal(transactionState({status:'ACCEPTED'}),'ACCEPTED');});
test('canonical explorer validation rejects malformed records',()=>{assert.equal(explorer('address','0x'+'12'.repeat(20)),'https://explorer-studio.genlayer.com/address/0x'+'12'.repeat(20));assert.throws(()=>explorer('address','0x123?fake=true'));assert.throws(()=>explorer('tx','0x'+'12'.repeat(20)));});
test('entry closes exactly at deadline',()=>{const m={status:'OPEN',spec:{entry_deadline:100}} as Market;assert.equal(closed(m,99),false);assert.equal(closed(m,100),true);});

import {parseWire} from '../lib/wire';
test('wei integers remain exact, quoted numbers remain data',()=>{assert.deepEqual(parseWire('{"amount":100000000000000000001,"quote":"say:100000000000000000001, never change it","option":1}'),{amount:'100000000000000000001',quote:'say:100000000000000000001, never change it',option:1});});

import {publicProof,type Proof} from '../lib/domain';
test('raw probes and previous releases never enter the initial payload',()=>{const p={contracts:{},transactions:{},markets:[],submissionReady:false,blockers:[],probes:{sample:'hidden spoiler'},previousReleases:[{outcome:'hidden spoiler'}]} as unknown as Proof;assert.ok(!JSON.stringify(publicProof(p)).includes('hidden spoiler'));});

test('majority disagreement is a finalized error even when leader execution succeeds',()=>{assert.equal(transactionState({status:'FINALIZED',result_name:'MAJORITY_DISAGREE',consensus_data:{leader_receipt:[{execution_result:'SUCCESS'}]}}),'FINALIZED_ERROR');});

test('historical compiled propositions cannot spoil a shielded card',()=>{const m={question:'Who wins?',spec:{rehearsal:true,proposition:'The eventual winner wins.'}} as Market;assert.ok(!JSON.stringify(shield(m)).includes('The eventual winner'));assert.equal(m.spec?.proposition,'The eventual winner wins.');});
