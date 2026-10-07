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
cmd_javac = f'javac -source 1.8 -target 1.8 -cp "{android_jar}" -d {bin_dir} tools/re_tools/src/com/droidlogic/app/OutputModeManager.java'
subprocess.run(cmd_javac, shell=True, check=True)

# 2. D8
dex_dir = 'tools/re_tools/dex_out'
cmd_d8 = f'{d8} --output {dex_dir} {bin_dir}/com/droidlogic/app/OutputModeManager.class'
subprocess.run(cmd_d8, shell=True, check=True)

# 3. Baksmali to smali
import zipfile
with zipfile.ZipFile('tools/re_tools/temp_omm.apk', 'w') as z:
    z.write('tools/re_tools/dex_out/classes.dex', 'classes.dex')

temp_dec = 'tools/re_tools/temp_omm_dec'
if os.path.exists(temp_dec):
    shutil.rmtree(temp_dec)
subprocess.run(f'java -jar {apktool} d -f tools/re_tools/temp_omm.apk -o {temp_dec}', shell=True, check=True)

src_smali = f'{temp_dec}/smali/com/droidlogic/app/OutputModeManager.smali'
dst_dir = 'tools/re_tools/tvsettings_decompiled/smali/com/droidlogic/app'
os.makedirs(dst_dir, exist_ok=True)
dst_smali = f'{dst_dir}/OutputModeManager.smali'
shutil.copy2(src_smali, dst_smali)

# 4. Build TV Settings APK
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

# 5. TEST DISPLAY ACTIVITY
print('=== [VERIFY 1] Starting DisplayActivity ===')
subprocess.run([adb, '-s', dev, 'logcat', '-c'], timeout=5)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n com.android.tv.settings/.display.DisplayActivity'], timeout=5)
time.sleep(1.5)
res1 = subprocess.run([adb, '-s', dev, 'logcat', '-d', '-s', 'AndroidRuntime'], capture_output=True, text=True)
print('Display Logcat:\n', res1.stdout)

# 6. TEST SOUND ACTIVITY + DOWN
print('=== [VERIFY 2] Starting SoundActivity + DOWN ===')
subprocess.run([adb, '-s', dev, 'logcat', '-c'], timeout=5)
subprocess.run([adb, '-s', dev, 'shell', 'am start -n com.android.tv.settings/.sound.SoundActivity'], timeout=5)
time.sleep(1)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'], timeout=5)
time.sleep(1.5)
res2 = subprocess.run([adb, '-s', dev, 'logcat', '-d', '-s', 'AndroidRuntime'], capture_output=True, text=True)
print('Sound Logcat:\n', res2.stdout)

res_focus = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys window windows | grep mCurrentFocus'], capture_output=True, text=True)
print('Final Window Focus:\n', res_focus.stdout)
