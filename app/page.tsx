import PlotApp from '@/components/app';
import {proof} from '@/lib/server';
import {shield} from '@/lib/domain';
export const dynamic='force-dynamic';
export default function Page(){const p=proof();return <PlotApp proof={{...p,markets:p.markets.map(shield)}}/>}
