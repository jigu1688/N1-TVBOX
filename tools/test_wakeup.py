import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
time.sleep(1)

# Wake up with keyevent 26
subprocess.run([adb, "-s", dev, "shell", "input keyevent 26"])
time.sleep(1)

r = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i mWakefulness="], capture_output=True, text=True)
print("After keyevent 26:", r.stdout.strip())

r2 = subprocess.run([adb, "-s", dev, "shell", "uptime"], capture_output=True, text=True)
print("Uptime:", r2.stdout.strip())
