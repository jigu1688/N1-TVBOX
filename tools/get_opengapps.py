import urllib.request
import os, zipfile, tarfile, shutil

# Sourceforge direct download URL for OpenGApps arm64 7.1 pico
url = 'https://downloads.sourceforge.net/project/opengapps/arm64/20220215/open_gapps-arm64-7.1-pico-20220215.zip'
zip_path = 'tools/open_gapps-arm64-7.1-pico-20220215.zip'

if not os.path.exists(zip_path):
    print(f'[*] Downloading OpenGApps 7.1 ARM64 Pico from SourceForge...')
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=120) as response, open(zip_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    print(f'[+] Downloaded: {zip_path} ({os.path.getsize(zip_path) / 1024 / 1024:.2f} MB)')
else:
    print(f'[+] Already exists: {zip_path} ({os.path.getsize(zip_path) / 1024 / 1024:.2f} MB)')

# Extract GApps components
extract_dir = 'tools/gapps_extracted'
if os.path.exists(extract_dir):
    shutil.rmtree(extract_dir)
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_dir)

print('[+] Extracted OpenGApps ZIP. Contents:')
for root, dirs, files in os.walk(extract_dir):
    for f in files:
        if f.endswith('.tar.lz') or f.endswith('.tar') or f.endswith('.apk'):
            print('  -', os.path.relpath(os.path.join(root, f), extract_dir))
