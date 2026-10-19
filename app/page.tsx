import PlotApp from '@/components/app';
import {proof} from '@/lib/server';
import {publicProof} from '@/lib/domain';
export const dynamic='force-dynamic';
export default function Page(){const p=proof();return <PlotApp proof={publicProof(p)}/>}
