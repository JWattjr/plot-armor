"""Run dependent release stages sequentially; never race proof.json writers."""
import subprocess,sys
for stage in sys.argv[1:]:
    result=subprocess.run([sys.executable,'scripts/release.py',stage])
    if result.returncode:raise SystemExit(result.returncode)
