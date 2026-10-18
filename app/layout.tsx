import type {Metadata} from 'next';
import '@fontsource/barlow-condensed/600.css';
import '@fontsource/barlow-condensed/700.css';
import '@fontsource/dm-sans/400.css';
import '@fontsource/dm-sans/500.css';
import '@fontsource/dm-sans/600.css';
import './globals.css';
export const metadata:Metadata={title:'Plot Armor — your watchlist, your call',description:'Bet on your favourite shows. GenLayer validators read the episode and settle it — spoiler-free.'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
