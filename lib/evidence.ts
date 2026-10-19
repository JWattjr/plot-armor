export function wikipediaRevision(article:string,revision:number){
 if(!article||article.length>2000||!Number.isSafeInteger(revision)||revision<1)throw Error('Invalid Wikipedia revision');
 return `https://en.wikipedia.org/w/index.php?title=${encodeURIComponent(article)}&oldid=${revision}&action=raw`;
}
