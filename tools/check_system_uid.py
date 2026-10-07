import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], capture_output=True, timeout=5)

def sh(cmd):
    r = subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace", timeout=5)
    return r.stdout.strip()

print("=== MOUNT ===")
print(sh("mount | grep system"))

print("=== SU BINARY ===")
print(sh("ls -la /system/xbin/su /system/bin/su"))

print("=== INIT RC SERVICES ===")
print(sh("grep -h '^service ' /init*.rc /etc/init*.rc 2>/dev/null"))
