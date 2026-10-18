import subprocess,sys
from pathlib import Path
for p in sorted(Path('tests/direct').glob('test_*.py')):
    r=subprocess.run([sys.executable,'-m','pytest',str(p),'-q'])
    if r.returncode:raise SystemExit(r.returncode)
