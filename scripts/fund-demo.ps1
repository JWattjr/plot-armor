$ErrorActionPreference='Stop'
Set-Location -LiteralPath (Split-Path -Parent $PSScriptRoot)
$approval=Get-Content -LiteralPath '.secrets/deposit-approval.json' | ConvertFrom-Json
if($approval.approvedDepositWei -ne '11'){throw 'Owner approval for 11 wei is required.'}
if(Test-Path -LiteralPath 'deploy/funding.json'){Get-Content -LiteralPath 'deploy/funding.json';exit 0}
$wallet=& python -c "import sys;sys.path.insert(0,'scripts');from chain import signer;print(signer().address)"
$previousOptions=$env:NODE_OPTIONS
try {
 $env:NODE_OPTIONS=($previousOptions+' --import=./scripts/explicit-fees.mjs').Trim()
 $ErrorActionPreference='Continue'
 $output=& 'C:\Users\User\AppData\Roaming\npm\genlayer.cmd' account send $wallet 11 --account moment-grid-studionet --network studionet 2>&1
 $ErrorActionPreference='Stop'
 $output | Write-Output
 if($LASTEXITCODE -ne 0){throw 'Funding command failed; inspect before retrying.'}
 $hash=[regex]::Matches(($output -join "`n"),'0x[0-9a-fA-F]{64}') | Select-Object -Last 1 -ExpandProperty Value
 if(!$hash){throw 'No durable funding hash. Do not repeat blindly.'}
 @{approvedDepositWei='11';wallet=$wallet;wei='11';hash=$hash} | ConvertTo-Json | Set-Content -LiteralPath 'deploy/funding.json'
} finally {$env:NODE_OPTIONS=$previousOptions}
