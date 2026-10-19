export function errorMessage(error:unknown):string {
 const value=error&&typeof error==='object'?error as {code?:unknown;message?:unknown}:null;
 if(Number(value?.code)===-32002)return 'A wallet request is already pending. Open MetaMask and complete or reject it before trying again.';
 if(Number(value?.code)===4001)return 'Wallet request rejected. You can try again when ready.';
 if(typeof value?.message==='string'&&value.message.trim())return value.message;
 if(typeof error==='string'&&error.trim())return error;
 return 'The request failed. Open your wallet and try again.';
}
