"""Run dependent release stages sequentially; never race proof.json writers."""
import argparse,subprocess,sys,time
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--retry',type=int,default=1,choices=range(1,4),help='At most three resumable stage attempts, with 30-second backoff.')
parser.add_argument('stages',nargs='+')
args=parser.parse_args()
for stage in args.stages:
    for attempt in range(args.retry):
        result=subprocess.run([sys.executable,'scripts/release.py',stage])
        if not result.returncode:break
        if attempt+1<args.retry:
            print(stage,'failed; resuming saved state in 30 seconds',flush=True)
            time.sleep(30)
    if result.returncode:raise SystemExit(result.returncode)
