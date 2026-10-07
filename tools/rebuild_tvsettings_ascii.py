import os
import subprocess
import shutil
import tempfile

def recompile_tvsettings():
    src_dir = os.path.abspath("tools/re_tools/tvsettings_decompiled")
    temp_dir = r"C:\Users\jigu\AppData\Local\Temp\tvsettings_rebuild_work"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    shutil.copytree(src_dir, temp_dir)

    java = r"C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\java.exe"
    apktool_jar = os.path.abspath("tools/re_tools/apktool.jar")
    temp_apk = os.path.join(temp_dir, "temp_built.apk")
    
    print("[*] Rebuilding with apktool in ASCII temp dir...")
    subprocess.run([java, "-jar", apktool_jar, "b", temp_dir, "-o", temp_apk], check=True)

    zipalign = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
    aligned_apk = os.path.join(temp_dir, "aligned.apk")
    print("[*] Running zipalign...")
    subprocess.run([zipalign, "-p", "-f", "4", temp_apk, aligned_apk], check=True)

    debug_ks = os.path.expanduser('~/.android/debug.keystore')
    apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"
    signed_apk = os.path.abspath("tools/re_tools/PhiTvSettings_Signed.apk")
    print("[*] Signing with debug key...")
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{signed_apk}" "{aligned_apk}"', shell=True, check=True)

    dest = os.path.abspath("build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk")
    shutil.copy2(signed_apk, dest)
    print(f"[+] Recompiled and signed PhiTvSettings successfully: {os.path.getsize(signed_apk)} bytes!")

if __name__ == '__main__':
    recompile_tvsettings()
