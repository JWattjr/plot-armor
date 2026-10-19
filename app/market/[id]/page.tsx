import PlotApp from '@/components/app';
import {proof} from '@/lib/server';
import {publicProof} from '@/lib/domain';
export const dynamic='force-dynamic';
export default async function Page({params,searchParams}:{params:Promise<{id:string}>;searchParams:Promise<{option?:string}>}){const {id}=await params;const p=proof();const option=Number((await searchParams).option??0);const m=p.markets.find(m=>m.id===id);const initialOption=Number.isInteger(option)&&option>=0&&option<(m?.spec?.options.length??0)?option:0;return <PlotApp key={id+':'+initialOption} route="market" id={id} initialOption={initialOption} proof={publicProof(p)}/>}
