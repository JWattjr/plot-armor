"""Audit every HTTP URL in README and docs, including the Portal draft."""
import json,re,time
from pathlib import Path
from datetime import datetime,timezone
from urllib.parse import urlsplit,quote
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

ROOT=Path(__file__).resolve().parent.parent
REPORT=ROOT/'docs/link-audit.json'

def inventory():
    found={}
    for path in [ROOT/'README.md',*(ROOT/'docs').rglob('*')]:
        if not path.is_file() or path.suffix.lower() not in ('.md','.json','.txt'):continue
        content=path.read_text(encoding='utf-8-sig',errors='replace')
        for href in re.findall(r'\]\(([^)\s]+)\)',content):
            if not href.startswith(('http:','https:','#','mailto:')):
                target=(path.parent/href.split('#')[0]).resolve()
                if target.is_file() and target.is_relative_to(ROOT):
                    remote='https://github.com/JWattjr/plot-armor/blob/main/'+quote(target.relative_to(ROOT).as_posix(),safe='/')
                    found.setdefault(remote,set()).add(str(path.relative_to(ROOT)).replace('\\','/'))
        for url in re.findall(r'https?://[^\s<>"\x27`]+',content):
            url=url.rstrip('.,;:')
            if url.endswith(')') and url.count(')')>url.count('('):url=url[:-1]
            found.setdefault(url,set()).add(str(path.relative_to(ROOT)).replace('\\','/'))
    return found

def main():
    session=requests.Session();session.headers['User-Agent']='Mozilla/5.0 PlotArmorLinkAudit/1.0'
    session.mount('https://',HTTPAdapter(max_retries=Retry(total=2,backoff_factor=2,status_forcelist=[429,500,502,503,504],allowed_methods=['GET'])))
    rows=[];counts={'contract':0,'transaction':0,'other':0};failures=[]
    for url,files in sorted(inventory().items()):
        kind='other';target=url;expected=None
        try:
            if urlsplit(url).hostname=='explorer-studio.genlayer.com':
                contract=re.fullmatch(r'https://explorer-studio\.genlayer\.com/address/(0x[0-9a-fA-F]{40})',url)
                transaction=re.fullmatch(r'https://explorer-studio\.genlayer\.com/tx/(0x[0-9a-fA-F]{64})',url)
                api_contract=re.fullmatch(r'https://explorer-studio\.genlayer\.com/api/address/(0x[0-9a-fA-F]{40})',url)
                api_transaction=re.fullmatch(r'https://explorer-studio\.genlayer\.com/api/transactions/(0x[0-9a-fA-F]{64})',url)
                # Archived diagnostics legitimately cite the required API itself.
                # API references still need the real record, not an HTML 200.
                contract=contract or api_contract;transaction=transaction or api_transaction
                assert contract or transaction,'Non-canonical explorer URL'
                kind='contract' if contract else 'transaction';expected=(contract or transaction)[1]
                target='https://explorer-studio.genlayer.com/api/'+('address/' if contract else 'transactions/')+expected
            elif 'studio.genlayer.com/transactions/' in url:raise AssertionError('Non-canonical Studio transaction URL')
            counts[kind]+=1
            response=session.get(target,timeout=45)
            assert response.status_code==200,f'HTTP {response.status_code}'
            if kind=='contract':assert response.json().get('type')=='CONTRACT','Record is not CONTRACT'
            elif kind=='transaction':assert expected.lower() in json.dumps(response.json()).lower(),'Transaction record mismatch'
            rows.append({'url':url,'type':kind,'httpStatus':200,'recordVerified':kind!='other','files':sorted(files)})
            print('PASS',kind,url,flush=True)
        except Exception as error:
            failures.append({'url':url,'type':kind,'error':str(error),'files':sorted(files)})
            print('FAIL',url,str(error),flush=True)
        time.sleep(.5)
    report={'checkedAt':datetime.now(timezone.utc).isoformat(),'scope':'All distinct HTTP URLs in README.md and docs, including portal-fields.json and this report','counts':counts,'passed':len(rows),'failed':len(failures),'results':rows,'failures':failures}
    REPORT.write_text(json.dumps(report,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'counts':counts,'passed':len(rows),'failed':len(failures)}),flush=True)
    if failures:raise SystemExit(1)

if __name__=='__main__':main()
