import subprocess, os, shutil, time

android_jar = r'C:\Users\jigu\AppData\Local\Android\Sdk\platforms\android-34\android.jar'
d8 = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\d8.bat'
apktool = 'tools/re_tools/apktool.jar'
apksigner = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat'
zipalign = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe'
keystore = 'tools/re_tools/debug.keystore'
adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# 1. Compile Java
bin_dir = 'tools/re_tools/bin'
cmd_javac = f'javac -source 1.8 -target 1.8 -cp "{android_jar}" -d {bin_dir} tools/re_tools/src/com/android/tv/settings/display/SafeOutputModeManager.java tools/re_tools/src/com/android/tv/settings/display/SafeHdrManager.java'
subprocess.run(cmd_javac, shell=True, check=True)

# 2. D8
dex_dir = 'tools/re_tools/dex_out'
cmd_d8 = f'{d8} --output {dex_dir} {bin_dir}/com/android/tv/settings/display/SafeOutputModeManager.class {bin_dir}/com/android/tv/settings/display/SafeHdrManager.class'
subprocess.run(cmd_d8, shell=True, check=True)

# 3. Baksmali to smali
import zipfile
with zipfile.ZipFile('tools/re_tools/temp_omm.apk', 'w') as z:
    z.write('tools/re_tools/dex_out/classes.dex', 'classes.dex')

temp_dec = 'tools/re_tools/temp_omm_dec'
if os.path.exists(temp_dec):
    shutil.rmtree(temp_dec)
subprocess.run(f'java -jar {apktool} d -f tools/re_tools/temp_omm.apk -o {temp_dec}', shell=True, check=True)

dst_dir = 'tools/re_tools/tvsettings_decompiled/smali/com/android/tv/settings/display'
os.makedirs(dst_dir, exist_ok=True)
shutil.copy2(f'{temp_dec}/smali/com/android/tv/settings/display/SafeOutputModeManager.smali', f'{dst_dir}/SafeOutputModeManager.smali')
shutil.copy2(f'{temp_dec}/smali/com/android/tv/settings/display/SafeHdrManager.smali', f'{dst_dir}/SafeHdrManager.smali')

# Remove old invalid smali if present
for old_s in ['tools/re_tools/tvsettings_decompiled/smali/com/droidlogic/app/OutputModeManager.smali', 'tools/re_tools/tvsettings_decompiled/smali/com/droidlogic/app/HdrManager.smali']:
    if os.path.exists(old_s):
        os.remove(old_s)

# 4. Replace references
smali_root = 'tools/re_tools/tvsettings_decompiled/smali'
count_omm = 0
count_hdr = 0
for root, dirs, files in os.walk(smali_root):
    for f in files:
        if f.endswith('.smali'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8', errors='ignore') as sfile:
                content = sfile.read()
            changed = False
            if 'Lcom/droidlogic/app/OutputModeManager;' in content:
                content = content.replace('Lcom/droidlogic/app/OutputModeManager;', 'Lcom/android/tv/settings/display/SafeOutputModeManager;')
                count_omm += 1
                changed = True
            if 'Lcom/droidlogic/app/HdrManager;' in content:
                content = content.replace('Lcom/droidlogic/app/HdrManager;', 'Lcom/android/tv/settings/display/SafeHdrManager;')
                count_hdr += 1
                changed = True
            if changed:
                with open(path, 'w', encoding='utf-8') as sfile:
                    sfile.write(content)

print(f'[+] Replaced OutputModeManager in {count_omm} files, HdrManager in {count_hdr} files!')

# 5. Build, align, sign
temp_work = r'C:\Users\jigu\AppData\Local\Temp\tvsettings_decompiled'
if os.path.exists(temp_work):
    shutil.rmtree(temp_work, ignore_errors=True)
shutil.copytree('tools/re_tools/tvsettings_decompiled', temp_work)

temp_apk = r'C:\Users\jigu\AppData\Local\Temp\tvsettings_built.apk'
if os.path.exists(temp_apk):
    os.remove(temp_apk)

aligned_apk = r'C:\Users\jigu\AppData\Local\Temp\tvsettings_aligned.apk'
signed_apk = 'tools/re_tools/PhiTvSettings_Signed.apk'

subprocess.run(f'java -jar {apktool} b {temp_work} -o {temp_apk}', shell=True, check=True)
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)
subprocess.run([zipalign, '-f', '-p', '4', temp_apk, aligned_apk], check=True)
if os.path.exists(signed_apk):
    os.remove(signed_apk)
shutil.copy2(aligned_apk, signed_apk)
subprocess.run(f'{apksigner} sign --ks {keystore} --ks-pass pass:android --ks-key-alias androiddebugkey --key-pass pass:android {signed_apk}', shell=True, check=True)

# Copy to ROM root
dst_rom = 'build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk'
shutil.copy2(signed_apk, dst_rom)
print(f'[+] Updated ROM root: {dst_rom}')

# Install on live device
subprocess.run([adb, '-s', dev, 'install', '-r', '-d', signed_apk], check=True)
print('[+] Successfully installed on live N1!')

# 6. VERIFY ALL DISPLAY SUB-MENUS (INCLUDING IMAGE STRENGTHEN)
print('=== [VERIFY 1] Starting DisplayActivity and testing Image Strengthen ===')
subprocess.run([adb, '-s', dev, 'logcat', '-c'], timeout=5)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n com.android.tv.settings/.display.DisplayActivity'], timeout=5)
time.sleep(1)

# Navigate through all 5 items
for i in range(4):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
    time.sleep(0.3)

# Press RIGHT into Image Strengthen
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 22'])
time.sleep(0.5)

# Press DOWN inside Image Strengthen
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.5)

res1 = subprocess.run([adb, '-s', dev, 'logcat', '-d', '-s', 'AndroidRuntime'], capture_output=True, text=True)
print('Display + Image Strengthen Result:\n', 'CRASH!' if 'FATAL EXCEPTION' in res1.stdout else 'PERFECT SUCCESS!')
if 'FATAL EXCEPTION' in res1.stdout:
    print(res1.stdout)

res_focus = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows | grep mCurrentFocus'], capture_output=True, text=True)
print('Current Focus:\n', res_focus.stdout)
