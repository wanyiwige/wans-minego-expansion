$ErrorActionPreference='Stop'
$taskProject=Split-Path -Parent $PSScriptRoot
$taskInstance=Split-Path -Parent $taskProject
$taskRelease=Join-Path $taskProject 'build\libs\wans_minego_expansion-0.6.0.jar'
$taskOld=Join-Path $taskInstance 'mods\wans_minego_expansion-0.5.0.jar'
$taskInstalled=Join-Path $taskInstance 'mods\wans_minego_expansion-0.6.0.jar'
if(-not(Test-Path -LiteralPath $taskOld)){throw 'Expected current 0.5.0 JAR missing; inspect active variants before retrying.'}
if(Test-Path -LiteralPath $taskInstalled){throw '0.6.0 is already installed; inspect it before replacing.'}
$taskVariants=@(Get-ChildItem -LiteralPath (Join-Path $taskInstance 'mods') -Filter 'wans_minego_expansion*.jar' -File)
if($taskVariants.Count -ne 1){throw 'Expected exactly one current active target-mod JAR.'}
$taskReleaseHash=(Get-FileHash -LiteralPath $taskRelease -Algorithm SHA256).Hash
$taskOldHash=(Get-FileHash -LiteralPath $taskOld -Algorithm SHA256).Hash
$taskBackup=Join-Path $taskInstance ('backups\20261010-'+(Get-Date -Format HHmmss)+'-before-exploration-souls-0.6.0')
New-Item -ItemType Directory -Path $taskBackup | Out-Null
$taskBackupJar=Join-Path $taskBackup 'wans_minego_expansion-0.5.0.jar'
Copy-Item -LiteralPath $taskOld -Destination $taskBackupJar
if((Get-FileHash -LiteralPath $taskBackupJar -Algorithm SHA256).Hash -ne $taskOldHash){throw 'Rollback backup hash mismatch.'}
$taskStage=Join-Path $taskInstance '.codex_staging\wans_minego_expansion-0.6.0.jar'
New-Item -ItemType Directory -Path (Split-Path -Parent $taskStage) -Force | Out-Null
Copy-Item -LiteralPath $taskRelease -Destination $taskStage -Force
if((Get-FileHash -LiteralPath $taskStage -Algorithm SHA256).Hash -ne $taskReleaseHash){throw 'Staged release hash mismatch.'}
# Named-file moves only; the predecessor is preserved and the verified rollback copy already exists.
Move-Item -LiteralPath $taskOld -Destination (Join-Path $taskBackup 'original-active-0.5.0.jar')
try {
    Move-Item -LiteralPath $taskStage -Destination $taskInstalled
    if((Get-FileHash -LiteralPath $taskInstalled -Algorithm SHA256).Hash -ne $taskReleaseHash){throw 'Installed JAR hash mismatch.'}
} catch {
    if(-not(Test-Path -LiteralPath $taskOld)){Copy-Item -LiteralPath $taskBackupJar -Destination $taskOld}
    throw
}
$taskRemaining=@(Get-ChildItem -LiteralPath (Join-Path $taskInstance 'mods') -Filter 'wans_minego_expansion*.jar' -File)
if($taskRemaining.Count -ne 1){throw 'Unexpected active variant count after installation.'}
$taskReceipt=[ordered]@{
 version='0.6.0'; release=$taskRelease; installed=$taskInstalled;
 release_sha256=$taskReleaseHash; installed_sha256=(Get-FileHash -LiteralPath $taskInstalled -Algorithm SHA256).Hash;
 old_sha256=$taskOldHash; rollback_jar=$taskBackupJar;
 source_backup='wans-minego-expansion/backups/20261010-184652-before-biome-souls';
 old_texture_count=32; new_texture_count=19; new_finished_items=19; attuned_ingredients=1;
 build='BUILD SUCCESSFUL; reobfJar executed; dev verification class excluded';
 independent_forge_checks=[ordered]@{foolish_present=89; foolish_absent=3; phase='ServerStartingEvent before third-party network initialization'};
 full_test_server_startup='blocked by local loopback connection error in IronsLib PatreonHandler initialization';
 pack_restart_verified=$false; gameplay_verified=$false
}
$taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskBackup 'deployment.json') -Encoding utf8
$taskReceipt | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $taskProject 'audit\20261010-biome-souls\release-receipt.json') -Encoding utf8
Write-Output "Installed: $taskInstalled"
Write-Output "SHA256: $taskReleaseHash"
Write-Output "Rollback: $taskBackupJar"
