import {NextResponse} from 'next/server';
import {market,proof} from '@/lib/server';
import {shield} from '@/lib/domain';
export async function GET(request:Request,context:{params:Promise<{id:string}>}){try{const {id}=await context.params;const p=new URL(request.url).searchParams;const recorded=p.get('source')==='recorded';const value=recorded?proof().markets.find(m=>m.id===id):await market(id);if(!value)throw Error('Market not found');return NextResponse.json({market:p.get('reveal')==='yes'?value:shield(value),source:recorded?'RECORDED_PROOF':'LIVE_FINALIZED',readAt:recorded?proof().recordedAt:new Date().toISOString()})}catch(e){return NextResponse.json({error:e instanceof Error?e.message:'Read failed'},{status:503})}}
