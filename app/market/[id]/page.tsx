import PlotApp from '@/components/app';
import {proof} from '@/lib/server';
import {shield} from '@/lib/domain';
export const dynamic='force-dynamic';
export default async function Page({params}:{params:Promise<{id:string}>}){const {id}=await params;const p=proof();return <PlotApp route="market" id={id} proof={{...p,markets:p.markets.map(shield)}}/>}
