import os
import shutil
import subprocess
import zipfile

def build_webpush_apk():
    print("="*60)
    print("  Building NextGen 隔空传装 TV APK (com.nextgen.webpush)")
    print("="*60)

    src_proj = os.path.abspath('tools/webpush_project')
    temp_proj = r'C:\Users\jigu\AppData\Local\Temp\webpush_build'
    if os.path.exists(temp_proj):
        shutil.rmtree(temp_proj)
    shutil.copytree(src_proj, temp_proj)

    sdk_dir = os.path.expanduser(r'~\AppData\Local\Android\Sdk')
    build_tools = os.path.join(sdk_dir, 'build-tools', '36.0.0')
    android_jar = os.path.join(sdk_dir, 'platforms', 'android-34', 'android.jar')
    zxing_jar = os.path.join(temp_proj, 'libs', 'zxing-core.jar')
    
    aapt2 = os.path.join(build_tools, 'aapt2.exe')
    d8 = os.path.join(build_tools, 'd8.bat')
    zipalign = os.path.join(build_tools, 'zipalign.exe')
    apksigner = os.path.join(build_tools, 'apksigner.bat')
    debug_ks = os.path.expanduser('~/.android/debug.keystore')
    javac = r'C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\javac.EXE'

    bin_dir = os.path.join(temp_proj, 'bin')
    dex_dir = os.path.join(temp_proj, 'dex')
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(dex_dir, exist_ok=True)

    compiled_res = os.path.join(temp_proj, 'compiled_res.zip')
    unaligned_apk = os.path.join(temp_proj, 'app_unaligned.apk')
    aligned_apk = os.path.join(temp_proj, 'app_aligned.apk')
    temp_signed_apk = os.path.join(temp_proj, 'app_signed.apk')
    out_apk = os.path.abspath('NextGen_隔空传装_v1.0.apk')

    # 1. Compile Resources with aapt2
    print('[*] Compiling resources with aapt2 from ASCII path...')
    subprocess.run([aapt2, 'compile', '--dir', os.path.join(temp_proj, 'res'), '-o', compiled_res], check=True)

    # 2. Link Resources
    print('[*] Linking resources with aapt2...')
    manifest = os.path.join(temp_proj, 'AndroidManifest.xml')
    src_dir = os.path.join(temp_proj, 'src')
    subprocess.run([aapt2, 'link', '-I', android_jar, '--manifest', manifest, '-o', unaligned_apk, compiled_res, '--java', src_dir, '--auto-add-overlay'], check=True)

    # 3. Compile Java with javac
    print('[*] Compiling Java classes with ZXing...')
    java_files = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.java'):
                java_files.append(os.path.join(root, f))
    classpath = f"{android_jar};{zxing_jar}"
    subprocess.run([javac, '-encoding', 'UTF-8', '-source', '1.8', '-target', '1.8', '-cp', classpath, '-d', bin_dir] + java_files, check=True)

    # 4. Dex classes with D8 (merging ZXing classes)
    print('[*] Converting bytecode to Dalvik DEX with D8...')
    class_files = []
    for root, dirs, files in os.walk(bin_dir):
        for f in files:
            if f.endswith('.class'):
                class_files.append(os.path.join(root, f))
    
    cmd_d8 = f'call "{d8}" --min-api 25 --output "{dex_dir}" "{zxing_jar}" ' + ' '.join([f'"{cf}"' for cf in class_files])
    subprocess.run(cmd_d8, shell=True, check=True)

    # 5. Add classes.dex into unaligned APK
    print('[*] Adding classes.dex into APK package...')
    classes_dex = os.path.join(dex_dir, 'classes.dex')
    with zipfile.ZipFile(unaligned_apk, 'a', compression=zipfile.ZIP_DEFLATED) as apk_zip:
        apk_zip.write(classes_dex, 'classes.dex')

    # 6. Zipalign
    print('[*] Zipaligning APK...')
    subprocess.run([zipalign, '-p', '-f', '4', unaligned_apk, aligned_apk], check=True)

    # 7. Sign APK
    print('[*] Signing APK with keystore...')
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{temp_signed_apk}" "{aligned_apk}"', shell=True, check=True)

    # 8. Copy to target destination
    shutil.copy2(temp_signed_apk, out_apk)
    os.makedirs('tools', exist_ok=True)
    shutil.copy2(temp_signed_apk, 'tools/WebPush.apk')
    print(f'[+] SUCCESS! Generated standalone APK with official ZXing: {out_apk}')

if __name__ == '__main__':
    build_webpush_apk()
