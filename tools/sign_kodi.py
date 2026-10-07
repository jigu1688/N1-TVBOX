import os
import zipfile
import subprocess

def sign_kodi():
    src = 'tools/Kodi_19.5_Matrix_arm64_zh.apk'
    unsigned = 'tools/kodi_unsigned.apk'
    
    print("[*] Removing old signatures...")
    with zipfile.ZipFile(src, 'r') as zin, zipfile.ZipFile(unsigned, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if not item.filename.startswith('META-INF/'):
                zout.writestr(item, zin.read(item.filename))

    zipalign = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
    aligned = 'tools/kodi_aligned.apk'
    print("[*] Running zipalign 4...")
    subprocess.run([zipalign, "-p", "-f", "4", unsigned, aligned], check=True)

    debug_ks = os.path.expanduser('~/.android/debug.keystore')
    if not os.path.exists(debug_ks):
        os.makedirs(os.path.dirname(debug_ks), exist_ok=True)
        cmd_kt = f'keytool -genkey -v -keystore "{debug_ks}" -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000 -dname "CN=Android Debug,O=Android,C=US"'
        subprocess.run(cmd_kt, shell=True, check=True)

    apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"
    signed = 'tools/Kodi_19.5_Matrix_arm64_zh_signed.apk'
    print("[*] Signing APK with apksigner...")
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{signed}" "{aligned}"', shell=True, check=True)
    print(f"[+] Signed successfully: {signed} ({os.path.getsize(signed)} bytes)")

if __name__ == '__main__':
    sign_kodi()
