import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)

# 1. Check current timeout
r = subprocess.run([adb, "-s", dev, "shell", "settings get system screen_off_timeout"], capture_output=True, text=True)
orig_timeout = r.stdout.strip()
print(f"Original screen_off_timeout: {orig_timeout}")

# 2. Set to 1000ms (1 second)
print("Setting screen_off_timeout to 1000ms...")
subprocess.run([adb, "-s", dev, "shell", "settings put system screen_off_timeout 1000"])

time.sleep(3)

r = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i mWakefulness="], capture_output=True, text=True)
print("Wakefulness after 3s:", r.stdout.strip())

# Restore
subprocess.run([adb, "-s", dev, "shell", f"settings put system screen_off_timeout {orig_timeout}"])
