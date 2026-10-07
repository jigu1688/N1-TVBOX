import os
import subprocess
import zipfile
import shutil

print("[1] Compiling Smali to classes.dex...")
cmd_smali = "java -jar tools/re_tools/smali.jar a tools/re_tools/atv_decompiled/smali -o tools/re_tools/new_classes.dex"
res = subprocess.run(cmd_smali, shell=True, capture_output=True, text=True)
print(res.stdout, res.stderr)

dex_file = "tools/re_tools/new_classes.dex"
print(f"[+] Compiled classes.dex: {os.path.getsize(dex_file)} bytes")

orig_apk = "ATV Launcher Pro v0.2.1.apk"
unsigned_apk = "tools/re_tools/atv_unsigned.apk"
aligned_apk = "tools/re_tools/atv_aligned.apk"
signed_apk = "tools/re_tools/ATVLauncher_Custom_Hardcoded.apk"

# Replace classes.dex
print("[2] Replacing classes.dex in APK...")
with zipfile.ZipFile(orig_apk, 'r') as zin:
    with zipfile.ZipFile(unsigned_apk, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename.startswith('META-INF/') or item.filename == 'classes.dex':
                continue
            zout.writestr(item, zin.read(item.filename))
        with open(dex_file, "rb") as f:
            zout.writestr("classes.dex", f.read())

# Zipalign
print("[3] Zipaligning APK...")
zipalign = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
if os.path.exists(aligned_apk):
    os.remove(aligned_apk)
subprocess.run([zipalign, "-f", "-p", "4", unsigned_apk, aligned_apk], check=True)

# Sign with apksigner
print("[4] Signing APK...")
apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"
keystore = "tools/re_tools/debug.keystore"
if not os.path.exists(keystore):
    cmd_key = f'keytool -genkey -v -keystore {keystore} -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=AndroidDebug,O=Android,C=US"'
    subprocess.run(cmd_key, shell=True, check=True)

if os.path.exists(signed_apk):
    os.remove(signed_apk)
shutil.copy2(aligned_apk, signed_apk)

cmd_sign = f'{apksigner} sign --ks {keystore} --ks-pass pass:android --ks-key-alias androiddebugkey --key-pass pass:android {signed_apk}'
subprocess.run(cmd_sign, shell=True, check=True)

# Also update system_root
target_system_apk = "build_rom/system_root/app/ATVLauncher/ATVLauncher.apk"
shutil.copy2(signed_apk, target_system_apk)

print(f"[+] SUCCESS! Generated & Updated: {signed_apk} ({os.path.getsize(signed_apk)} bytes)")
