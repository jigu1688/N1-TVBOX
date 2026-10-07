import urllib.request
import subprocess
import os
import zipfile
import shutil

os.makedirs('tools/re_tools', exist_ok=True)

# Download smali-2.5.2.jar
smali_jar_url = "https://bitbucket.org/JesusFreke/smali/downloads/smali-2.5.2.jar"
smali_jar = "tools/re_tools/smali.jar"

if not os.path.exists(smali_jar):
    print("Downloading smali.jar...")
    try:
        urllib.request.urlretrieve(smali_jar_url, smali_jar)
        print("Downloaded smali.jar:", os.path.getsize(smali_jar), "bytes")
    except Exception as e:
        print("Download failed:", e)

# 1. Compile smali to classes.dex using smali.jar
print("[1] Compiling modified Smali -> classes.dex...")
cmd_smali = f'java -jar tools/re_tools/smali.jar a tools/re_tools/atv_decompiled/smali -o tools/re_tools/new_classes.dex'
res = subprocess.run(cmd_smali, shell=True, capture_output=True, text=True)
print("Smali assemble output:\n", res.stdout, res.stderr)

if not os.path.exists("tools/re_tools/new_classes.dex"):
    # Fallback to apktool with --no-src or d8 if needed
    print("Trying apktool build...")
    cmd_apktool = "java -Dfile.encoding=utf-8 -jar tools/re_tools/apktool.jar b -f tools/re_tools/atv_decompiled -o tools/re_tools/atv_temp.apk"
    res2 = subprocess.run(cmd_apktool, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(res2.stdout, res2.stderr)
    if os.path.exists("tools/re_tools/atv_temp.apk"):
        with zipfile.ZipFile("tools/re_tools/atv_temp.apk") as z:
            z.extract("classes.dex", "tools/re_tools")
            os.rename("tools/re_tools/classes.dex", "tools/re_tools/new_classes.dex")

print("New classes.dex size:", os.path.getsize("tools/re_tools/new_classes.dex"))

# 2. Inject new_classes.dex into original APK
orig_apk = "ATV Launcher Pro v0.2.1.apk"
custom_apk_unsigned = "tools/re_tools/ATVLauncher_Custom_Unsigned.apk"

shutil.copy2(orig_apk, custom_apk_unsigned)

# Update zip with new classes.dex
print("[2] Replacing classes.dex in APK...")
# Read all entries from orig_apk except META-INF and classes.dex
with zipfile.ZipFile(orig_apk, 'r') as zin:
    with zipfile.ZipFile(custom_apk_unsigned, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename.startswith('META-INF/') or item.filename == 'classes.dex':
                continue
            zout.writestr(item, zin.read(item.filename))
        # Add new classes.dex
        with open("tools/re_tools/new_classes.dex", "rb") as f:
            zout.writestr("classes.dex", f.read())

print("[3] Signing custom APK with testkey...")
# Find apksigner or use jarsigner
keystore = "tools/re_tools/debug.keystore"
if not os.path.exists(keystore):
    cmd_key = f'keytool -genkey -v -keystore {keystore} -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=AndroidDebug,O=Android,C=US"'
    subprocess.run(cmd_key, shell=True, capture_output=True)

final_custom_apk = "tools/re_tools/ATVLauncher_Custom_Hardcoded.apk"
shutil.copy2(custom_apk_unsigned, final_custom_apk)

cmd_sign = f'jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {keystore} -storepass android {final_custom_apk} androiddebugkey'
subprocess.run(cmd_sign, shell=True, capture_output=True)

print(f"[+] COMPLETE! Generated signed custom APK: {final_custom_apk} ({os.path.getsize(final_custom_apk)} bytes)")
