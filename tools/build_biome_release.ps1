param([switch]$Verification)
$ErrorActionPreference = 'Stop'
$taskProject = Split-Path -Parent $PSScriptRoot
$taskJava = 'D:\game\PCL\jdk\jdk-17.0.20.1+1\bin\java.exe'
$taskGradle = 'C:\Users\WANYIWIGE\.gradle\wrapper\dists\gradle-8.8-bin\dl7vupf4psengwqhwktix4v1\gradle-8.8'
$taskClasspath = ((Get-ChildItem -LiteralPath "$taskGradle\lib" -Filter '*.jar' -File | Select-Object -ExpandProperty FullName) -join ';')
$taskArguments = @(
 '--add-opens=java.base/java.util=ALL-UNNAMED', '--add-opens=java.base/java.lang=ALL-UNNAMED',
 '--add-opens=java.base/java.lang.invoke=ALL-UNNAMED', '--add-opens=java.prefs/java.util.prefs=ALL-UNNAMED',
 '--add-opens=java.base/java.nio.charset=ALL-UNNAMED', '--add-opens=java.base/java.net=ALL-UNNAMED',
 '--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED', '-Dfile.encoding=GBK',
 '-Duser.country=CN', '-Duser.language=zh', '-Duser.variant',
 "-javaagent:$taskGradle\lib\agents\gradle-instrumentation-agent-8.8.jar",
 '-cp', $taskClasspath, 'org.gradle.launcher.Main', 'clean', 'build', '--offline', '--no-daemon'
)
if($Verification) {
 $taskArguments += '-PbiomeVerification'
 & 'C:\Users\WANYIWIGE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' "$PSScriptRoot\write_verification_structure.py"
}
Push-Location $taskProject
try {
 $taskLog = if($Verification) {'build-biome-verification.log'} else {'build-biome-souls.log'}
 & $taskJava @taskArguments *> $taskLog
 $taskExit = $LASTEXITCODE
 Get-Content -LiteralPath $taskLog -Tail 32
 if($taskExit -ne 0) { throw "Gradle failed with exit code $taskExit; see $taskLog" }
} finally { Pop-Location }
