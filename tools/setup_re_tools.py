import urllib.request
import os

os.makedirs('tools/re_tools', exist_ok=True)

# 1. Download apktool.jar
apktool_url = "https://github.com/iBotPeaches/Apktool/releases/download/v2.9.3/apktool_2.9.3.jar"
apktool_path = "tools/re_tools/apktool.jar"

# Also fallback to fast mirrors if needed
print("Downloading apktool.jar...")
try:
    urllib.request.urlretrieve(apktool_url, apktool_path)
    print("Downloaded apktool.jar:", os.path.getsize(apktool_path), "bytes")
except Exception as e:
    print("Download failed:", e)

# 2. Extract APK classes.dex directly using zipfile for static analysis
import zipfile
apk_path = "build_rom/system_root/app/ATVLauncher/ATVLauncher.apk"
with zipfile.ZipFile(apk_path) as z:
    for name in z.namelist():
        if name.endswith('.dex') or 'assets' in name or 'res/xml' in name:
            print("APK entry:", name)
            z.extract(name, "tools/re_tools/apk_extracted")

print("APK assets and dex extracted!")
