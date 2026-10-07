import subprocess
import os
import shutil

import sys
cmd_build = "java -jar tools/re_tools/apktool.jar b tools/re_tools/atv_decompiled -o tools/re_tools/ATVLauncher_unsigned.apk"
res = subprocess.run(cmd_build, shell=True, capture_output=True)
sys.stdout.buffer.write(b"Apktool stdout:\n" + res.stdout + b"\n")
if res.stderr:
    sys.stdout.buffer.write(b"Apktool stderr:\n" + res.stderr + b"\n")

if not os.path.exists("tools/re_tools/ATVLauncher_unsigned.apk"):
    raise RuntimeError("Apktool build failed!")

print(f"[+] Built unsigned APK: {os.path.getsize('tools/re_tools/ATVLauncher_unsigned.apk')} bytes")

# Sign with debug / platform key
print("[2] Signing APK with testkey/apksigner...")
# Check if apksigner exists in Android SDK
android_sdk_apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools"
apksigner_path = None
for root, dirs, files in os.walk(android_sdk_apksigner):
    if "apksigner.bat" in files or "apksigner.jar" in files:
        apksigner_path = os.path.join(root, "apksigner.jar") if "apksigner.jar" in files else os.path.join(root, "apksigner.bat")
        break

signed_apk = "tools/re_tools/ATVLauncher_Custom_Signed.apk"

# Also fallback to python-based zip signer or jarsigner / uber-apk-signer
if apksigner_path:
    print(f"Found apksigner: {apksigner_path}")
    # generate a keystore if not exist
    keystore = "tools/re_tools/debug.keystore"
    if not os.path.exists(keystore):
        cmd_key = f'keytool -genkey -v -keystore {keystore} -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=AndroidDebug,O=Android,C=US"'
        subprocess.run(cmd_key, shell=True, capture_output=True)
    
    if apksigner_path.endswith('.jar'):
        cmd_sign = f'java -jar "{apksigner_path}" sign --ks {keystore} --ks-pass pass:android --out {signed_apk} tools/re_tools/ATVLauncher_unsigned.apk'
    else:
        cmd_sign = f'"{apksigner_path}" sign --ks {keystore} --ks-pass pass:android --out {signed_apk} tools/re_tools/ATVLauncher_unsigned.apk'
    
    s_res = subprocess.run(cmd_sign, shell=True, capture_output=True)
    sys.stdout.buffer.write(b"Sign output:\n" + s_res.stdout + b"\n" + s_res.stderr + b"\n")
else:
    print("apksigner not found in SDK, using jarsigner...")
    keystore = "tools/re_tools/debug.keystore"
    if not os.path.exists(keystore):
        cmd_key = f'keytool -genkey -v -keystore {keystore} -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=AndroidDebug,O=Android,C=US"'
        subprocess.run(cmd_key, shell=True, capture_output=True)
    shutil.copy2("tools/re_tools/ATVLauncher_unsigned.apk", signed_apk)
    subprocess.run(f'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {keystore} -storepass android {signed_apk} androiddebugkey', shell=True)

if os.path.exists(signed_apk):
    print(f"[+] Successfully generated signed custom APK: {signed_apk} ({os.path.getsize(signed_apk)} bytes)")
else:
    print("[-] Signing failed!")
