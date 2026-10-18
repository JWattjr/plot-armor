import {NextResponse} from 'next/server';
import {read} from '@/lib/server';
export async function GET(request:Request){try{const p=new URL(request.url).searchParams;const value=await read(p.get('contract')??'',p.get('method')??'',JSON.parse(p.get('args')??'[]'));return NextResponse.json({value,source:'LIVE_FINALIZED',readAt:new Date().toISOString()})}catch(e){return NextResponse.json({error:e instanceof Error?e.message:'Read failed'},{status:503})}}
