import zipfile
import shutil
import os

# 1. Restore pristine framework-res from extracted_aml
shutil.copy2('extracted_aml/system_root/framework/framework-res.apk', 'build_rom/system_root/framework/framework-res.apk.base')

# 2. Only inject config_webview_packages.xml into framework-res.apk without touching resources.arsc!
# Let's get compiled config_webview_packages.xml
compiled_webview_xml = None
if os.path.exists('build_rom/system_root/framework/framework-res.apk'):
    with zipfile.ZipFile('build_rom/system_root/framework/framework-res.apk', 'r') as z:
        if 'res/xml/config_webview_packages.xml' in z.namelist():
            compiled_webview_xml = z.read('res/xml/config_webview_packages.xml')

tmp_out = 'build_rom/system_root/framework/framework-res-pure.apk'
with zipfile.ZipFile('build_rom/system_root/framework/framework-res.apk.base', 'r') as zin:
    with zipfile.ZipFile(tmp_out, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            if item.filename == 'res/xml/config_webview_packages.xml' and compiled_webview_xml:
                continue
            zout.writestr(item, zin.read(item.filename))
        if compiled_webview_xml:
            zout.writestr('res/xml/config_webview_packages.xml', compiled_webview_xml)

shutil.copy2(tmp_out, 'build_rom/system_root/framework/framework-res.apk')
print(f"[+] Pristine framework-res.apk restored (size: {os.path.getsize('build_rom/system_root/framework/framework-res.apk')} bytes)!")
