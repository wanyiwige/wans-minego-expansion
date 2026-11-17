$ErrorActionPreference = 'Stop'
$taskProject = Split-Path -Parent $PSScriptRoot
$taskInstance = Split-Path -Parent $taskProject
$taskMods = Join-Path $taskInstance 'mods'
$taskRelease = Join-Path $taskProject 'build/libs/wans_minego_expansion-0.7.5.jar'
$taskExpected = 'B24B32E0B69B39E7DC806F06CA14D0C2413193C76559475DE1CCCD1696A0D1CE'
if ((Get-FileHash -LiteralPath $taskRelease -Algorithm SHA256).Hash -ne $taskExpected) { throw 'Release differs from the validated artifact.' }
$taskOld = @(Get-ChildItem -LiteralPath $taskMods -File | Where-Object { $_.Name -match '^wans_minego_expansion.*\.jar$' })
if ($taskOld.Count -ne 1 -or $taskOld[0].Name -ne 'wans_minego_expansion-0.7.1.jar') { throw 'Unexpected installed version; inspect before deployment.' }
$taskOld = $taskOld[0]
$taskOldHash = (Get-FileHash -LiteralPath $taskOld.FullName -Algorithm SHA256).Hash
$taskBackup = Join-Path $taskProject ('backups/20261020-before-0.7.5-deploy-' + [guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory -Path $taskBackup | Out-Null
$taskSaved = Join-Path $taskBackup $taskOld.Name
Copy-Item -LiteralPath $taskOld.FullName -Destination $taskSaved
if ((Get-FileHash -LiteralPath $taskSaved -Algorithm SHA256).Hash -ne $taskOldHash) { throw 'Backup hash mismatch.' }
$taskTarget = Join-Path $taskMods 'wans_minego_expansion-0.7.5.jar'
$taskPending = Join-Path $taskBackup 'wans_minego_expansion-0.7.5.jar.pending'
Copy-Item -LiteralPath $taskRelease -Destination $taskPending
if ((Get-FileHash -LiteralPath $taskPending -Algorithm SHA256).Hash -ne $taskExpected) { throw 'Staged release hash mismatch.' }
$taskRetired = Join-Path $taskBackup 'previous-active'
New-Item -ItemType Directory -Path $taskRetired | Out-Null
$taskRetiredFile = Join-Path $taskRetired $taskOld.Name
Move-Item -LiteralPath $taskOld.FullName -Destination $taskRetiredFile
try {
    Move-Item -LiteralPath $taskPending -Destination $taskTarget
} catch {
    Move-Item -LiteralPath $taskRetiredFile -Destination $taskOld.FullName
    throw
}
$taskDeployedHash = (Get-FileHash -LiteralPath $taskTarget -Algorithm SHA256).Hash
$taskActive = @(Get-ChildItem -LiteralPath $taskMods -File | Where-Object { $_.Name -match '^wans_minego_expansion.*\.jar$' })
if ($taskDeployedHash -ne $taskExpected -or $taskActive.Count -ne 1 -or $taskActive[0].Name -ne 'wans_minego_expansion-0.7.5.jar') { throw 'Deployment verification failed.' }
$taskReceipt = [ordered]@{
    clientDate='2026-10-20'; oldVersion='0.7.1'; newVersion='0.7.5'
    oldSHA256=$taskOldHash; backup=$taskSaved; backupVerified=$true
    retiredOriginal=$taskRetiredFile; installed=$taskTarget; installedSHA256=$taskDeployedHash
    singleActiveJar=$true; restarted=$false; gameplayVerified=$false
}
$taskReceipt | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $taskBackup 'deployment.json') -Encoding UTF8
$taskReceipt | ConvertTo-Json
