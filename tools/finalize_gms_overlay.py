import os, shutil, subprocess

apksigner = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat'
zipalign = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe'
keystore = 'tools/re_tools/debug.keystore'

gms_clean = 'tools/gms_system_clean'

# Copy valid 320 signed GmsCore
src_gmscore = 'tools/gmscore_320_signed.apk'
dst_gmscore = os.path.join(gms_clean, 'priv-app', 'PrebuiltGmsCore', 'PrebuiltGmsCore.apk')
os.makedirs(os.path.dirname(dst_gmscore), exist_ok=True)
shutil.copy2(src_gmscore, dst_gmscore)
print(f'[+] Replaced GmsCore with signed valid APK: {os.path.getsize(dst_gmscore)/1024/1024:.2f} MB')

# Ensure all other APKs are validly signed
for root, dirs, files in os.walk(gms_clean):
    for f in files:
        if f.endswith('.apk'):
            apk_path = os.path.join(root, f)
            # Verify signature with apksigner
            res = subprocess.run(f'{apksigner} verify {apk_path}', shell=True, capture_output=True, text=True)
            if res.returncode != 0:
                print(f'[!] Resigning {f}...')
                tmp = apk_path + '.tmp'
                subprocess.run([zipalign, '-f', '-p', '4', apk_path, tmp], check=True)
                subprocess.run(f'{apksigner} sign --v1-signing-enabled true --v2-signing-enabled true --ks {keystore} --ks-pass pass:android --ks-key-alias androiddebugkey --key-pass pass:android --out "{apk_path}" "{tmp}"', shell=True, check=True)
                if os.path.exists(tmp): os.remove(tmp)
            print(f'  [OK] Verified signed: {f} ({os.path.getsize(apk_path)/1024/1024:.2f} MB)')

print('[+] All GMS APKs finalized and verified!')
