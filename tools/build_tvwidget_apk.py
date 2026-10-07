import os
import shutil
import subprocess
import zipfile

def build_tvwidget_apk():
    print("="*60)
    print("  Building NextGen TV Dashboard Widget APK (com.nextgen.tvwidget)")
    print("="*60)

    src_proj = os.path.abspath('tools/tvwidget_project')
    temp_proj = r'C:\Users\jigu\AppData\Local\Temp\tvwidget_build'
    if os.path.exists(temp_proj):
        shutil.rmtree(temp_proj)
    shutil.copytree(src_proj, temp_proj)

    sdk_dir = os.path.expanduser(r'~\AppData\Local\Android\Sdk')
    build_tools = os.path.join(sdk_dir, 'build-tools', '36.0.0')
    android_jar = os.path.join(sdk_dir, 'platforms', 'android-34', 'android.jar')
    
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
    out_apk = os.path.abspath('NextGen_TVWidget_v1.0.apk')

    # 1. Compile Resources with aapt2
    print('[*] Compiling resources with aapt2...')
    subprocess.run([aapt2, 'compile', '--dir', os.path.join(temp_proj, 'res'), '-o', compiled_res], check=True)

    # 2. Link Resources
    print('[*] Linking resources with aapt2...')
    manifest = os.path.join(temp_proj, 'AndroidManifest.xml')
    src_dir = os.path.join(temp_proj, 'src')
    subprocess.run([aapt2, 'link', '-I', android_jar, '--manifest', manifest, '-o', unaligned_apk, compiled_res, '--java', src_dir, '--auto-add-overlay'], check=True)

    # 3. Compile Java with javac
    print('[*] Compiling Java classes...')
    java_files = []
    for root, dirs, files in os.walk(src_dir):
        for f in files:
            if f.endswith('.java'):
                java_files.append(os.path.join(root, f))
    subprocess.run([javac, '-encoding', 'UTF-8', '-source', '1.8', '-target', '1.8', '-cp', android_jar, '-d', bin_dir] + java_files, check=True)

    # 4. Dex classes with D8
    print('[*] Converting bytecode to Dalvik DEX with D8...')
    class_files = []
    for root, dirs, files in os.walk(bin_dir):
        for f in files:
            if f.endswith('.class'):
                class_files.append(os.path.join(root, f))
    subprocess.run([d8, '--lib', android_jar, '--output', dex_dir] + class_files, check=True)

    # 5. Add classes.dex into APK
    print('[*] Adding classes.dex into APK package...')
    classes_dex = os.path.join(dex_dir, 'classes.dex')
    with zipfile.ZipFile(unaligned_apk, 'a') as zip_apk:
        zip_apk.write(classes_dex, 'classes.dex')

    # 6. Zipalign APK
    print('[*] Zipaligning APK...')
    subprocess.run([zipalign, '-f', '-p', '4', unaligned_apk, aligned_apk], check=True)

    # 7. Sign APK
    print('[*] Signing APK with keystore...')
    if not os.path.exists(debug_ks):
        keytool = r'C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\keytool.EXE'
        os.makedirs(os.path.dirname(debug_ks), exist_ok=True)
        subprocess.run([keytool, '-genkeypair', '-alias', 'androiddebugkey', '-keypass', 'android', '-keystore', debug_ks, '-storepass', 'android', '-dname', 'CN=Android Debug,O=Android,C=US', '-validity', '10000', '-keyalg', 'RSA', '-keysize', '2048'], check=True)

    subprocess.run([apksigner, 'sign', '--ks', debug_ks, '--ks-pass', 'pass:android', '--key-pass', 'pass:android', '--ks-key-alias', 'androiddebugkey', '--out', temp_signed_apk, aligned_apk], check=True)

    # 8. Copy to output
    shutil.copy2(temp_signed_apk, out_apk)
    shutil.copy2(temp_signed_apk, 'tools/NextGen_TVWidget.apk')
    print(f"[+] SUCCESS! Generated standalone TV Widget APK: {out_apk}")

if __name__ == '__main__':
    build_tvwidget_apk()
