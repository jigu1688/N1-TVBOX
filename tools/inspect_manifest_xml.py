import subprocess, os, shutil, re

apktool = 'tools/re_tools/apktool.jar'
apk = 'tools/gapps_components/gmscore-arm64/gmscore-arm64/nodpi/priv-app/PrebuiltGmsCore/PrebuiltGmsCore.apk'
out_dec = 'tools/gmscore_dec'

if os.path.exists(out_dec):
    shutil.rmtree(out_dec)

subprocess.run(f'java -jar {apktool} d -f -s "{apk}" -o "{out_dec}"', shell=True, check=True)
manifest_file = os.path.join(out_dec, 'AndroidManifest.xml')
with open(manifest_file, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print(f'Manifest XML text decoded! Length: {len(text)} chars')
# Search for compileSdkVersion or high api attributes
matches = re.findall(r'<manifest[^>]+>', text)
for m in matches:
    print('Manifest root tag:\n', m)

# Also check for any unknown attributes or high sdk attributes
for attr in ['compileSdkVersion', 'platformBuildVersionCode', 'isolatedSplits', 'appComponentFactory', 'allowNativeHeapPointerTagging']:
    if attr in text:
        print(f'Found attribute: {attr}')
