import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

def ensure_conn():
    subprocess.run([adb, "connect", dev], stdout=subprocess.DEVNULL)

def sh(cmd):
    ensure_conn()
    p = subprocess.run([adb, "-s", dev, "shell", cmd], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return p.stdout.decode('utf-8', errors='ignore').strip()

print("=== 2. Input devices ===")
print(sh("getevent -S"))

print("\n=== 3. Keylayout files in /system/usr/keylayout ===")
print(sh("ls -la /system/usr/keylayout/"))

print("\n=== 4. Check props ===")
print(sh("getprop | grep -i -E 'power|shutdown|sleep|suspend'"))

print("\n=== 5. Check PhoneWindowManager power key behavior ===")
print(sh("dumpsys window policy | grep -i -E 'power|press'"))
