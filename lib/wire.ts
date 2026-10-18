/** Preserve wei-sized JSON integers without changing numbers inside strings. */
export function parseWire(text:string):unknown{
 let output='',i=0;
 while(i<text.length){
  if(text[i]==='"'){const start=i++;while(i<text.length){if(text[i]==='\\'){i+=2;continue}if(text[i++]==='"')break}output+=text.slice(start,i);continue}
  if(text[i]==='-'||/[0-9]/.test(text[i])){const start=i++;while(i<text.length&&/[\d.eE+-]/.test(text[i]))i++;const token=text.slice(start,i);output+=/^-?\d+$/.test(token)&&(!Number.isSafeInteger(Number(token)))?JSON.stringify(token):token;continue}
  output+=text[i++];
 }
 return JSON.parse(output);
}
