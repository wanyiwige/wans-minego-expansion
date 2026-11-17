param([switch]$Verification)
$ErrorActionPreference='Stop'
$taskProject=Split-Path -Parent $PSScriptRoot
$taskJava='D:\game\PCL\jdk\jdk-17.0.20.1+1\bin\java.exe'
$taskGradle='C:\Users\WANYIWIGE\.gradle\wrapper\dists\gradle-8.8-bin\dl7vupf4psengwqhwktix4v1\gradle-8.8'
$taskClasspath=((Get-ChildItem -LiteralPath "$taskGradle\lib" -Filter '*.jar' -File | Select-Object -ExpandProperty FullName) -join ';')
$taskArguments=@(
 '--add-opens=java.base/java.util=ALL-UNNAMED','--add-opens=java.base/java.lang=ALL-UNNAMED',
 '--add-opens=java.base/java.lang.invoke=ALL-UNNAMED','--add-opens=java.prefs/java.util.prefs=ALL-UNNAMED',
 '--add-opens=java.base/java.nio.charset=ALL-UNNAMED','--add-opens=java.base/java.net=ALL-UNNAMED',
 '--add-opens=java.base/java.util.concurrent.atomic=ALL-UNNAMED','-Dfile.encoding=GBK',
 '-Duser.country=CN','-Duser.language=zh','-Duser.variant',
 "-javaagent:$taskGradle\lib\agents\gradle-instrumentation-agent-8.8.jar",
 '-cp',$taskClasspath,'org.gradle.launcher.Main','clean','build','--offline','--no-daemon',
 # ForgeGradle pings remote certificate hosts even in offline mode. Only cached dependencies are used here.
 '-Dnet.minecraftforge.gradle.check.certs=false'
)
if($Verification){$taskArguments+='-PepochVerification'}
Push-Location $taskProject
try {
 $taskLog=if($Verification){'build-epoch-verification.log'}else{'build-epoch-souls.log'}
 & $taskJava @taskArguments *> $taskLog
 $taskExit=$LASTEXITCODE
 Get-Content -LiteralPath $taskLog -Tail 24
 if($taskExit -ne 0){throw "Gradle failed: $taskExit. See $taskLog"}
}finally{Pop-Location}
