import subprocess, zipfile, shutil, os

temp_work = r'C:\Users\jigu\AppData\Local\Temp\framework_decompiled'
if os.path.exists(temp_work):
    shutil.rmtree(temp_work, ignore_errors=True)
shutil.copytree('build_rom/framework_decompiled', temp_work)

temp_out = r'C:\Users\jigu\AppData\Local\Temp\framework_new.apk'
if os.path.exists(temp_out):
    os.remove(temp_out)

apktool = 'tools/re_tools/apktool.jar'
cmd = f'java -jar {apktool} b "{temp_work}" -o "{temp_out}"'
print(f"[*] Running apktool b...")
p = subprocess.run(cmd, shell=True)

if os.path.exists(temp_out):
    with zipfile.ZipFile(temp_out, 'r') as znew:
        compiled_webview = znew.read('res/xml/config_webview_packages.xml')
        compiled_manifest = znew.read('AndroidManifest.xml')

    orig_apk = 'build_rom/system_root/framework/framework-res.apk'
    backup_apk = 'build_rom/system_root/framework/framework-res.apk.bak'
    if not os.path.exists(backup_apk):
        shutil.copy2(orig_apk, backup_apk)

    tmp_apk = 'build_rom/framework_temp.apk'
    with zipfile.ZipFile(backup_apk, 'r') as zin:
        with zipfile.ZipFile(tmp_apk, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename in ['res/xml/config_webview_packages.xml', 'AndroidManifest.xml']:
                    continue
                zout.writestr(item, zin.read(item.filename))
            zout.writestr('res/xml/config_webview_packages.xml', compiled_webview)
            zout.writestr('AndroidManifest.xml', compiled_manifest)

    shutil.copy2(tmp_apk, orig_apk)
    if os.path.exists(tmp_apk):
        os.remove(tmp_apk)
    print(f'[+] Successfully injected updated AndroidManifest.xml & config_webview_packages.xml into framework-res.apk! ({os.path.getsize(orig_apk)} bytes)')
else:
    print('[-] Error: framework_new.apk was not generated.')
