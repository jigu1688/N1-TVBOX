import subprocess, os, shutil

android_jar = r'C:\Users\jigu\AppData\Local\Android\Sdk\platforms\android-34\android.jar'
d8 = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\d8.bat'
baksmali = 'tools/re_tools/baksmali.jar'

# Compile Java
bin_dir = 'tools/re_tools/bin'
os.makedirs(bin_dir, exist_ok=True)

cmd_javac = f'javac -source 1.8 -target 1.8 -cp "{android_jar}" -d {bin_dir} tools/re_tools/src/com/droidlogic/app/OutputModeManager.java'
subprocess.run(cmd_javac, shell=True, check=True)

# D8 to classes.dex
dex_dir = 'tools/re_tools/dex_out'
os.makedirs(dex_dir, exist_ok=True)
cmd_d8 = f'{d8} --output {dex_dir} {bin_dir}/com/droidlogic/app/OutputModeManager.class'
subprocess.run(cmd_d8, shell=True, check=True)

# Baksmali to smali
smali_target_dir = 'tools/re_tools/tvsettings_decompiled/smali'
cmd_bak = f'java -jar {baksmali} d {dex_dir}/classes.dex -o {smali_target_dir}'
subprocess.run(cmd_bak, shell=True, check=True)

print('[+] Successfully injected safe OutputModeManager.smali!')
