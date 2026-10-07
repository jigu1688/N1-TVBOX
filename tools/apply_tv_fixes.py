import os
import shutil

def apply_tv_fixes():
    print("[*] Applying TV Launcher, U-Boot USB Boot & Logo fixes...")
    
    # 1. Update logo.PARTITION in package directory (remove Phicomm Butler advertisement)
    src_logo = 'extracted_webpad/logo.PARTITION'
    dst_logo = 'build_rom/package/logo.PARTITION'
    if os.path.exists(src_logo):
        shutil.copy2(src_logo, dst_logo)
        print(f"[+] Replaced logo.PARTITION with clean TV logo (removed Phicomm Butler image)")
        
    # 2. Add U-Disk Boot App (Reboot.apk) into system/app/Reboot
    reboot_dir = 'build_rom/system_root/app/Reboot'
    os.makedirs(reboot_dir, exist_ok=True)
    shutil.copy2('tools/Reboot.apk', os.path.join(reboot_dir, 'Reboot.apk'))
    print(f"[+] Installed Reboot.apk (One-click U-Disk Boot / Recovery / Restart) into system/app/Reboot")
    
    # 3. Add RootExplorer & Terminal into system/app
    re_dir = 'build_rom/system_root/app/RootExplorer'
    os.makedirs(re_dir, exist_ok=True)
    shutil.copy2('tools/RootExplorer.apk', os.path.join(re_dir, 'RootExplorer.apk'))
    
    term_dir = 'build_rom/system_root/app/Terminal'
    os.makedirs(term_dir, exist_ok=True)
    shutil.copy2('tools/Terminal.apk', os.path.join(term_dir, 'Terminal.apk'))
    print(f"[+] Installed RootExplorer and Terminal utilities")
    
    # 4. Ensure Launchers are located in both app and priv-app for guaranteed startup
    # Place Lighthome in priv-app and app
    for p_dir in ['build_rom/system_root/priv-app/Lighthome', 'build_rom/system_root/app/Lighthome']:
        os.makedirs(p_dir, exist_ok=True)
        shutil.copy2('extracted_webpad/system_root/app/Lighthome/Lighthome.apk', os.path.join(p_dir, 'Lighthome.apk'))
        
    for p_dir in ['build_rom/system_root/priv-app/TVLauncher', 'build_rom/system_root/app/TVLauncher']:
        os.makedirs(p_dir, exist_ok=True)
        shutil.copy2('extracted_webpad/system_root/app/tvlauncher/tvlauncher.apk', os.path.join(p_dir, 'TVLauncher.apk'))
    print("[+] Deployed Lighthome and TVLauncher into system/priv-app & system/app")
    
    # 5. Add /system/bin/reboot-update script for command-line USB boot
    reboot_update_script = "build_rom/system_root/bin/reboot-update"
    with open(reboot_update_script, 'w', encoding='utf-8', newline='\n') as f:
        f.write("#!/system/bin/sh\n/system/bin/reboot update\n")
    print("[+] Added /system/bin/reboot-update script")
    
    # 6. Update build.prop to disable setup wizard and ensure instant home launch
    bp_path = 'build_rom/system_root/build.prop'
    with open(bp_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    extra_props = [
        "ro.setupwizard.mode=DISABLED",
        "ro.setupwizard.require_network=none",
        "ro.setupwizard.user_req=0",
        "persist.sys.usb.config=adb",
        "service.adb.tcp.port=5555",
        "service.phiadb.root=1",
        "persist.sys.cibn.auth_disabled=1"
    ]
    
    lines = [l for l in content.splitlines() if not any(l.startswith(p.split('=')[0] + '=') for p in extra_props)]
    for ep in extra_props:
        lines.append(ep)
        
    with open(bp_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines) + '\n')
    print("[+] Updated build.prop with ro.setupwizard.mode=DISABLED and ADB configurations")

if __name__ == '__main__':
    apply_tv_fixes()
