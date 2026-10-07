import zipfile
import subprocess
import os

# Let's extract original classes.dex from ATV Launcher Pro v0.2.1.apk and disassemble only LauncherDatabase_Impl$a.smali
orig_apk = "ATV Launcher Pro v0.2.1.apk"
with zipfile.ZipFile(orig_apk, 'r') as z:
    z.extract('classes.dex', 'tools/re_tools/orig_dex')

# Baksmali
cmd_bak = "java -jar tools/re_tools/apktool.jar d -f ATV Launcher Pro v0.2.1.apk -o tools/re_tools/orig_decomp"
# or just look at orig_decomp if exists
res = subprocess.run('java -jar tools/re_tools/apktool.jar d -f "ATV Launcher Pro v0.2.1.apk" -o tools/re_tools/orig_decomp', shell=True, capture_output=True, text=True)

with open('tools/re_tools/orig_decomp/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali', 'r', encoding='utf-8') as f:
    for i in range(50):
        print(f.readline(), end='')
