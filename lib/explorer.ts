const origin = 'https://explorer-studio.genlayer.com';
export function explorer(kind: 'address' | 'tx' | 'addressApi' | 'txApi', value: string) {
  if (!(kind.startsWith('address') ? /^0x[\da-f]{40}$/i : /^0x[\da-f]{64}$/i).test(value)) throw Error('Invalid explorer record');
  const route={address:'address',tx:'tx',addressApi:'api/address',txApi:'api/transactions'}[kind];
  return `${origin}/${route}/${value}`;
}
