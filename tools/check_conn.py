import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

print("Trying to connect to 192.168.31.115:5555...")
r = subprocess.run([adb, "connect", dev], capture_output=True, text=True, timeout=5)
print("Connect output:", r.stdout.strip())

r = subprocess.run([adb, "-s", dev, "shell", "uptime"], capture_output=True, text=True, timeout=5)
print("Uptime:", r.stdout.strip())
