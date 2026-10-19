import test from 'node:test';
import assert from 'node:assert/strict';
import {errorMessage} from '../lib/errors';
import {needsTransactionPolling} from '../lib/domain';

test('plain EIP-1193 errors provide a recovery action',()=>{
 assert.match(errorMessage({code:-32002,message:'request pending'}),/Open MetaMask.*complete or reject/);
 assert.match(errorMessage({code:4001,message:'user denied'}),/rejected/);
 assert.equal(errorMessage({message:'RPC unavailable'}),'RPC unavailable');
 assert.equal(errorMessage(new Error('Source unavailable')),'Source unavailable');
 assert.doesNotMatch(errorMessage({}),/object Object/);
});

test('finality does not cancel a missing state read-back',()=>{
 assert.equal(needsTransactionPolling({state:'ACCEPTED'}),true);
 assert.equal(needsTransactionPolling({state:'FINALIZED_SUCCESS'}),true);
 assert.equal(needsTransactionPolling({state:'FINALIZED_SUCCESS',readback:[]}),false);
 assert.equal(needsTransactionPolling({state:'FINALIZED_SUCCESS',readback:null}),false);
 assert.equal(needsTransactionPolling({state:'FINALIZED_ERROR'}),false);
});
