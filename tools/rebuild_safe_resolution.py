import subprocess
import os
import shutil
import zipfile

def main():
    print("[1] Compiling Java...")
    android_jar = r"C:\Users\jigu\AppData\Local\Android\Sdk\platforms\android-34\android.jar"
    d8 = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\d8.bat"
    apktool = os.path.abspath("tools/re_tools/apktool.jar")
    zipalign = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe"
    apksigner = r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat"
    keystore = os.path.abspath("tools/re_tools/debug.keystore")
    
    bin_dir = os.path.abspath("tools/re_tools/bin")
    os.makedirs(bin_dir, exist_ok=True)

    src_omm = os.path.abspath("tools/re_tools/src/com/android/tv/settings/display/SafeOutputModeManager.java")
    src_hdr = os.path.abspath("tools/re_tools/src/com/android/tv/settings/display/SafeHdrManager.java")
    src_sleep = os.path.abspath("tools/re_tools/src/com/android/tv/settings/SafeSleepManager.java")

    cmd_javac = f'javac -source 1.8 -target 1.8 -cp "{android_jar}" -d "{bin_dir}" "{src_omm}" "{src_hdr}" "{src_sleep}"'
    subprocess.run(cmd_javac, shell=True, check=True)
    print("    javac OK")

    print("[2] Running D8...")
    dex_dir = os.path.abspath("tools/re_tools/dex_out")
    os.makedirs(dex_dir, exist_ok=True)
    all_classes = []
    for root_dir, _, files in os.walk(bin_dir):
        for f in files:
            if f.endswith(".class"):
                all_classes.append(f'"{os.path.join(root_dir, f)}"')
    cmd_d8 = f'"{d8}" --output "{dex_dir}" ' + ' '.join(all_classes)
    subprocess.run(cmd_d8, shell=True, check=True)
    print("    D8 OK")

    print("[3] Baksmaling via apktool...")
    temp_omm_apk = os.path.abspath("tools/re_tools/temp_omm.apk")
    with zipfile.ZipFile(temp_omm_apk, "w") as z:
        z.write(os.path.join(dex_dir, "classes.dex"), "classes.dex")

    temp_dec = os.path.abspath("tools/re_tools/temp_omm_dec")
    if os.path.exists(temp_dec):
        shutil.rmtree(temp_dec)
    subprocess.run(f'java -jar "{apktool}" d -f "{temp_omm_apk}" -o "{temp_dec}"', shell=True, check=True)

    # Copy all generated smali files to tvsettings_decompiled/smali
    smali_src_root = os.path.join(temp_dec, "smali")
    smali_dst_root = os.path.abspath("tools/re_tools/tvsettings_decompiled/smali")
    for root_dir, _, files in os.walk(smali_src_root):
        rel_dir = os.path.relpath(root_dir, smali_src_root)
        target_dir = os.path.join(smali_dst_root, rel_dir)
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            if f.endswith(".smali"):
                shutil.copy2(os.path.join(root_dir, f), os.path.join(target_dir, f))
    print("    Injected all updated smali files successfully!")

    print("[4] Building tvsettings APK in pure ASCII temp directory...")
    temp_work = r"C:\Users\jigu\AppData\Local\Temp\tvsettings_decompiled"
    if os.path.exists(temp_work):
        shutil.rmtree(temp_work, ignore_errors=True)
    shutil.copytree("tools/re_tools/tvsettings_decompiled", temp_work)

    temp_apk = r"C:\Users\jigu\AppData\Local\Temp\tvsettings_built.apk"
    if os.path.exists(temp_apk):
        os.remove(temp_apk)
    aligned_apk = r"C:\Users\jigu\AppData\Local\Temp\tvsettings_aligned.apk"
    if os.path.exists(aligned_apk):
        os.remove(aligned_apk)

    subprocess.run(f'java -jar "{apktool}" b "{temp_work}" -o "{temp_apk}"', shell=True, check=True)
    print("    apktool b OK")

    print("[5] Zipalign...")
    subprocess.run([zipalign, "-f", "-p", "4", temp_apk, aligned_apk], check=True)
    print("    zipalign OK")

    print("[6] Apksigner...")
    signed_apk = os.path.abspath("tools/re_tools/PhiTvSettings_Signed.apk")
    if os.path.exists(signed_apk):
        os.remove(signed_apk)
    cmd_sign = f'call "{apksigner}" sign --ks "{keystore}" --ks-pass pass:android --ks-key-alias androiddebugkey --key-pass pass:android --out "{signed_apk}" "{aligned_apk}"'
    subprocess.run(cmd_sign, shell=True, check=True)
    print(f"    Signed PhiTvSettings successfully: {os.path.getsize(signed_apk)} bytes")

    print("[7] Deploying to build_rom...")
    dst_rom = os.path.abspath("build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk")
    os.makedirs(os.path.dirname(dst_rom), exist_ok=True)
    shutil.copy2(signed_apk, dst_rom)
    print(f"[+] Successfully deployed to {dst_rom} ({os.path.getsize(dst_rom)} bytes)!")

if __name__ == "__main__":
    main()
