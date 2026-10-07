import os
import shutil
import subprocess

def patch_atvlauncher():
    temp_atv = r'C:\Users\jigu\AppData\Local\Temp\atv_clean_src'
    temp_apk = r'C:\Users\jigu\AppData\Local\Temp\atv_clean.apk'
    temp_aligned = r'C:\Users\jigu\AppData\Local\Temp\atv_clean_aligned.apk'

    if os.path.exists(temp_atv):
        shutil.rmtree(temp_atv)

    java = r'C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\java.EXE'
    apktool = os.path.abspath('tools/apktool.jar')
    zipalign = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe'
    apksigner = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat'
    debug_ks = os.path.expanduser('~/.android/debug.keystore')

    print('[*] Decompiling ATV Launcher Pro...')
    subprocess.run([java, '-jar', apktool, 'd', 'ATV Launcher Pro v0.2.1.apk', '-o', temp_atv, '-f'], check=True)

    smali_path = os.path.join(temp_atv, 'smali', 't1', 'a.smali')
    with open(smali_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Target chunk:
    #     iget-object v8, v8, Landroid/content/pm/ActivityInfo;->packageName:Ljava/lang/String;
    #
    #     const-string v9, "it.activityInfo.packageName"
    #
    #     invoke-static {v8, v9}, Lo7/j;->d(Ljava/lang/Object;Ljava/lang/String;)V

    replacement = """    iget-object v8, v8, Landroid/content/pm/ActivityInfo;->packageName:Ljava/lang/String;

    const-string v9, "it.activityInfo.packageName"

    invoke-static {v8, v9}, Lo7/j;->d(Ljava/lang/Object;Ljava/lang/String;)V

    const-string v9, "com.android.provision"

    invoke-virtual {v8, v9}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v9

    if-eqz v9, :cond_add_app_custom

    goto :goto_0

    :cond_add_app_custom"""

    target = """    iget-object v8, v8, Landroid/content/pm/ActivityInfo;->packageName:Ljava/lang/String;

    const-string v9, "it.activityInfo.packageName"

    invoke-static {v8, v9}, Lo7/j;->d(Ljava/lang/Object;Ljava/lang/String;)V"""

    if target in content:
        content = content.replace(target, replacement, 1)
        with open(smali_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print('[+] Successfully injected Provision filter into ATV Launcher!')
    else:
        raise RuntimeError("Target smali sequence not found in t1/a.smali!")

    print('[*] Recompiling ATV Launcher Pro...')
    subprocess.run([java, '-jar', apktool, 'b', temp_atv, '-o', temp_apk], check=True)

    print('[*] Zipaligning...')
    subprocess.run([zipalign, '-p', '-f', '4', temp_apk, temp_aligned], check=True)

    print('[*] Signing APK...')
    out_apk = os.path.abspath('ATV Launcher Pro v0.2.1.apk')
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{out_apk}" "{temp_aligned}"', shell=True, check=True)
    
    # Also update build_rom/system_root/app/ATVLauncher/ATVLauncher.apk
    os.makedirs('build_rom/system_root/app/ATVLauncher', exist_ok=True)
    shutil.copy2('ATV Launcher Pro v0.2.1.apk', 'build_rom/system_root/app/ATVLauncher/ATVLauncher.apk')
    print(f'[+] Complete! Updated ATV Launcher Pro with automatic Provision filter: {out_apk}')

if __name__ == '__main__':
    patch_atvlauncher()
