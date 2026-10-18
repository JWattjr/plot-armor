import subprocess,sys
from pathlib import Path
for path in Path('contracts').glob('*.py'):
    result=subprocess.run([sys.executable,'-c','from genvm_linter.cli import cli; cli()','check',str(path),'--json'])
    if result.returncode:raise SystemExit(result.returncode)
