import subprocess, os

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)

# 1. Pull packages.xml
subprocess.run([adb, "-s", dev, "pull", "/data/system/packages.xml", "tools/re_tools/packages.xml"], check=True)

with open("tools/re_tools/packages.xml", "r", encoding="utf-8") as f:
    content = f.read()

# Replace protection levels in permission definitions
content = content.replace('name="android.permission.DEVICE_POWER" package="android" prot="signature"',
                          'name="android.permission.DEVICE_POWER" package="android" prot="normal"')
content = content.replace('name="android.permission.INJECT_EVENTS" package="android" prot="signature"',
                          'name="android.permission.INJECT_EVENTS" package="android" prot="normal"')

# Add granted permissions to com.android.tv.settings
target = '<package name="com.android.tv.settings"'
idx = content.find(target)
if idx != -1:
    perms_idx = content.find("<perms>", idx)
    if perms_idx != -1:
        insert_perms = '\n            <item name="android.permission.DEVICE_POWER" granted="true" flags="0" />\n            <item name="android.permission.INJECT_EVENTS" granted="true" flags="0" />'
        if 'name="android.permission.DEVICE_POWER"' not in content[perms_idx:perms_idx+1500]:
            content = content[:perms_idx+7] + insert_perms + content[perms_idx+7:]
            print("[+] Added DEVICE_POWER and INJECT_EVENTS to com.android.tv.settings in packages.xml")

with open("tools/re_tools/packages_modified.xml", "w", encoding="utf-8") as f:
    f.write(content)

# 2. Push back to device
print("[*] Pushing updated packages.xml to device...")
subprocess.run([adb, "-s", dev, "push", "tools/re_tools/packages_modified.xml", "/data/system/packages.xml"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 660 /data/system/packages.xml && chown system:system /data/system/packages.xml"], check=True)

# 3. Soft restart Android framework (zygote)
print("[*] Restarting Android framework to reload packages.xml...")
subprocess.run([adb, "-s", dev, "shell", "stop && start"], check=True)

print("[+] Done! Framework restarted.")
