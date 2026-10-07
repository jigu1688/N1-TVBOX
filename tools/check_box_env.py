import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], capture_output=True, timeout=5)

def sh(cmd):
    try:
        r = subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace", timeout=5)
        return r.stdout.strip()
    except Exception as e:
        return f"ERROR: {e}"

print("=== ID ===")
print("ADB id:", sh("id"))

print("=== PACKAGES.XML FOR TVSETTINGS ===")
print(sh("grep -A 25 'package name=\"com.android.tv.settings\"' /data/system/packages.xml"))

print("=== CHECK SYSTEM PRIV-APP PERMISSIONS ===")
print(sh("ls -l /system/priv-app/PhiTvSettings/PhiTvSettings.apk"))

print("=== DUMPSYS PACKAGE COM.ANDROID.TV.SETTINGS PERMISSIONS ===")
print(sh("dumpsys package com.android.tv.settings | grep -A 30 'grantedPermissions:'"))
