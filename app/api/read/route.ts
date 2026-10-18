import {NextResponse} from 'next/server';
import {read} from '@/lib/server';
export async function GET(request:Request){try{const p=new URL(request.url).searchParams;let value=await read(p.get('contract')??'',p.get('method')??'',JSON.parse(p.get('args')??'[]'));if(p.get('method')==='get_predictions'&&p.get('reveal')!=='yes'&&Array.isArray(value))value=value.map(row=>({...row,status:'SHIELDED',points:0}));return NextResponse.json({value,source:'LIVE_FINALIZED',readAt:new Date().toISOString()})}catch(e){return NextResponse.json({error:e instanceof Error?e.message:'Read failed'},{status:503})}}
