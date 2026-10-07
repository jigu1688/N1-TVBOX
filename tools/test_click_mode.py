import subprocess
import time
import os

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.111:5555"

def ensure_connected():
    for _ in range(3):
        r = subprocess.run([adb, "connect", dev], capture_output=True, text=True)
        if "connected" in r.stdout or "already connected" in r.stdout:
            break
        time.sleep(1)

def sh(cmd):
    ensure_connected()
    r = subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True)
    return r.stdout.strip()

print("Mode before:", sh("cat /sys/class/display/mode"))

# Clear logcat
sh("logcat -c")

# Press RIGHT (22)
print("Pressing RIGHT (22)...")
sh("input keyevent 22")
time.sleep(0.5)

# Press DOWN (20)
print("Pressing DOWN (20)...")
sh("input keyevent 20")
time.sleep(0.5)

# Press CENTER (23)
print("Pressing CENTER (23)...")
sh("input keyevent 23")
time.sleep(2)

print("Mode after:", sh("cat /sys/class/display/mode"))

# Screencap
sh("screencap -p /sdcard/keys.png")
subprocess.run([adb, "-s", dev, "pull", "/sdcard/keys.png", "tools/keys.png"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Screenshot saved to tools/keys.png")

logs = sh("logcat -d -v time")
print("=== LOGS ===")
for l in logs.splitlines():
    if any(k in l for k in ["OutputMode", "SafeOutput", "OutputUi", "tv.settings", "system_control"]):
        print(l)
