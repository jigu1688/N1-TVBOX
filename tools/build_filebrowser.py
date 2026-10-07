import shutil
import subprocess
import os

def build_filebrowser():
    temp_src = r'C:\Users\jigu\AppData\Local\Temp\fb_src'
    temp_apk = r'C:\Users\jigu\AppData\Local\Temp\fb_hd.apk'
    temp_aligned = r'C:\Users\jigu\AppData\Local\Temp\fb_aligned.apk'

    if os.path.exists(temp_src):
        shutil.rmtree(temp_src)
        
    shutil.copytree('tools/FileBrowser_src', temp_src)

    java = r'C:\Program Files\Eclipse Adoptium\jdk-25.0.2.10-hotspot\bin\java.EXE'
    apktool = os.path.abspath('tools/apktool.jar')
    zipalign = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\zipalign.exe'
    apksigner = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat'
    debug_ks = os.path.expanduser('~/.android/debug.keystore')

    print('[*] Compiling with apktool from ASCII path...')
    subprocess.run([java, '-jar', apktool, 'b', temp_src, '-o', temp_apk], check=True)

    print('[*] Zipaligning...')
    subprocess.run([zipalign, '-p', '-f', '4', temp_apk, temp_aligned], check=True)

    print('[*] Signing APK...')
    out_signed = os.path.abspath('tools/FileBrowser_TV_HD.apk')
    subprocess.run(f'call "{apksigner}" sign --ks "{debug_ks}" --ks-pass pass:android --out "{out_signed}" "{temp_aligned}"', shell=True, check=True)
    print(f'[+] Successfully built and signed: {out_signed}')

if __name__ == '__main__':
    build_filebrowser()
