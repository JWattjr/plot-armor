import test from 'node:test';
import assert from 'node:assert/strict';
import {errorMessage} from '../lib/errors';

test('plain EIP-1193 errors provide a recovery action',()=>{
 assert.match(errorMessage({code:-32002,message:'request pending'}),/Open MetaMask.*complete or reject/);
 assert.match(errorMessage({code:4001,message:'user denied'}),/rejected/);
 assert.equal(errorMessage({message:'RPC unavailable'}),'RPC unavailable');
 assert.equal(errorMessage(new Error('Source unavailable')),'Source unavailable');
 assert.doesNotMatch(errorMessage({}),/object Object/);
});
