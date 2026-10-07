import subprocess
import zipfile
import shutil
import os
import re

def update_framework_res_power_menu():
    print("[*] Decompiling framework-res.apk to update config_shortPressOnPowerBehavior...")
    
    temp_work = r'C:\Users\jigu\AppData\Local\Temp\framework_power_decompiled'
    if os.path.exists(temp_work):
        shutil.rmtree(temp_work, ignore_errors=True)
    
    apktool = 'tools/re_tools/apktool.jar'
    orig_apk = 'build_rom/system_root/framework/framework-res.apk'
    
    # 1. Decode
    res_dec = subprocess.run(['java', '-jar', apktool, 'd', '-f', orig_apk, '-o', temp_work], capture_output=True, text=True)
    print("  Apktool decode status:", res_dec.returncode)
    
    # 2. Modify integers.xml: config_shortPressOnPowerBehavior -> 4 (GlobalActions Menu)
    int_file = os.path.join(temp_work, 'res', 'values', 'integers.xml')
    if not os.path.exists(int_file):
        raise FileNotFoundError(f"Cannot find {int_file}")
        
    with open(int_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    print("  Current config_shortPressOnPowerBehavior:", re.findall(r'<integer name="config_shortPressOnPowerBehavior">(\d+)</integer>', content))
    
    # Replace shortPressOnPowerBehavior with 4 (GlobalActions power menu)
    new_content = re.sub(
        r'<integer name="config_shortPressOnPowerBehavior">\d+</integer>',
        r'<integer name="config_shortPressOnPowerBehavior">4</integer>',
        content
    )
    
    with open(int_file, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
        
    print("  Updated config_shortPressOnPowerBehavior to 4 (GlobalActions Menu).")
    
    # 3. Build new framework APK
    temp_out = r'C:\Users\jigu\AppData\Local\Temp\framework_power_new.apk'
    if os.path.exists(temp_out):
        os.remove(temp_out)
        
    print("  Recompiling framework resources...")
    res_b = subprocess.run(['java', '-jar', apktool, 'b', temp_work, '-o', temp_out], capture_output=True, text=True)
    print("  Apktool build status:", res_b.returncode)
    if res_b.returncode != 0:
        print("Build error:", res_b.stderr)
        raise RuntimeError("Failed to build framework-res.apk")
        
    # 4. Inject compiled resources.arsc and config_webview_packages.xml into official signed APK container
    with zipfile.ZipFile(temp_out, 'r') as znew:
        compiled_arsc = znew.read('resources.arsc')
        compiled_webview_xml = znew.read('res/xml/config_webview_packages.xml')
        
    tmp_apk = 'build_rom/framework_power_final.apk'
    with zipfile.ZipFile(orig_apk, 'r') as zin:
        with zipfile.ZipFile(tmp_apk, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename in ['resources.arsc', 'res/xml/config_webview_packages.xml']:
                    continue
                zout.writestr(item, zin.read(item.filename))
            zout.writestr('resources.arsc', compiled_arsc)
            zout.writestr('res/xml/config_webview_packages.xml', compiled_webview_xml)
            
    shutil.copy2(tmp_apk, orig_apk)
    print("[+] SUCCESS: Injected Option A (short-press Power Menu) into framework-res.apk!")

if __name__ == '__main__':
    update_framework_res_power_menu()
