import {NextResponse} from 'next/server';
import {transaction} from '@/lib/server';
export async function GET(_:Request,context:{params:Promise<{hash:string}>}){try{return NextResponse.json(await transaction((await context.params).hash))}catch(e){return NextResponse.json({error:e instanceof Error?e.message:'Receipt unavailable'},{status:503})}}
