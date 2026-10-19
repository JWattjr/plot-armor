import {notFound} from 'next/navigation';
import PlotApp from '@/components/app';
import {proof} from '@/lib/server';
import {publicProof} from '@/lib/domain';
export const dynamic='force-dynamic';
export default async function Page({params}:{params:Promise<{route:string}>}){const {route}=await params;if(!['propose','predictions','activity','proof'].includes(route))notFound();const p=proof();return <PlotApp route={route==='predictions'?'mine':route} proof={publicProof(p)}/>}
