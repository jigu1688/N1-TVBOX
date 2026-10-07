import subprocess, os

apk = 'tools/gms_system_clean/priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk'
out_dir = 'tools/gmscore_baksmali'

print("[*] Extracting DEX files from PrebuiltGmsCore.apk...")
import zipfile
with zipfile.ZipFile(apk, 'r') as z:
    for f in z.namelist():
        if f.endswith('.dex'):
            z.extract(f, out_dir)
            print(f"  Extracted {f}")

print("[*] Searching for class ibg in dex files...")
# Use baksmali if jar exists, or grep directly
dex_files = [os.path.join(out_dir, f) for f in os.listdir(out_dir) if f.endswith('.dex')]
print(f"Found {len(dex_files)} dex files.")
