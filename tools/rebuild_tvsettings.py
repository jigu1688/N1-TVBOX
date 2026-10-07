import os
import subprocess
import shutil

def recompile_and_sign_tvsettings():
    print("[*] Recompiling PhiTvSettings...")
    java = r"C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\java.exe"
    apktool_jar = os.path.abspath("tools/re_tools/apktool.jar")
    temp_apk = os.path.abspath("tools/tvsettings_rebuilt.apk")
    src_dir = os.path.abspath("tools/re_tools/tvsettings_decompiled")
    
    if os.path.exists(temp_apk):
        os.remove(temp_apk)

    # 1. Build with apktool
    cmd_build = [java, "-jar", apktool_jar, "b", src_dir, "-o", temp_apk]
    subprocess.run(cmd_build, check=True)

    # 2. Zipalign
    zipalign = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
    aligned_apk = os.path.abspath("tools/tvsettings_aligned.apk")
    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)
    print("[*] Running zipalign...")
    subprocess.run([zipalign, "-p", "-f", "4", temp_apk, aligned_apk], check=True)

    # 3. Sign with debug.keystore
    debug_ks = os.path.expanduser('~/.android/debug.keystore')
    apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"
    signed_apk = os.path.abspath("tools/re_tools/PhiTvSettings_Signed.apk")
    print("[*] Signing with debug key...")
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{signed_apk}" "{aligned_apk}"', shell=True, check=True)

    # 4. Copy to build_rom
    dest = os.path.abspath("build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copy2(signed_apk, dest)
    print(f"[+] Recompiled and signed PhiTvSettings successfully: {os.path.getsize(signed_apk)} bytes!")

if __name__ == '__main__':
    recompile_and_sign_tvsettings()
