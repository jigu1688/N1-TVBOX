import subprocess, os, shutil

apktool = 'tools/re_tools/apktool.jar'
apk = 'tools/gapps_components/gmscore-arm64/gmscore-arm64/nodpi/priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk'
out_dec = 'tools/gmscore_dec'

if os.path.exists(out_dec):
    shutil.rmtree(out_dec)

print('[*] Decompiling GmsCore Manifest with apktool...')
subprocess.run(f'java -jar {apktool} d -f -r -s "{apk}" -o "{out_dec}"', shell=True, check=True)
print('[+] Decompiled!')

manifest_file = os.path.join(out_dec, 'AndroidManifest.xml')
with open(manifest_file, 'r', encoding='utf-8', errors='ignore') as f:
    lines = f.readlines()

print(f'Total lines in manifest: {len(lines)}')
print('First 30 lines:')
for l in lines[:30]:
    print(l, end='')
