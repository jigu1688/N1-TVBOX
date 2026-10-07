import subprocess
import os

# Let's baksmali original APK directly with baksmali-2.5.2.jar
cmd = 'java -jar tools/re_tools/baksmali-2.5.2.jar d "ATV Launcher Pro v0.2.1.apk" -o tools/re_tools/pure_baksmali'
r = subprocess.run(cmd, shell=True, capture_output=True, text=True)
print("Baksmali result:", r.returncode, r.stderr)

p1 = "tools/re_tools/pure_baksmali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"
with open(p1, 'r', encoding='utf-8') as f:
    print(f.read()[:500])
