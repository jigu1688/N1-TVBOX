import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)

print("Current wakefulness:")
r = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i mWakefulness="], capture_output=True, text=True)
print(r.stdout.strip())

print("Testing input keyevent 223...")
subprocess.run([adb, "-s", dev, "shell", "input keyevent 223"], check=True)
time.sleep(1)

print("Wakefulness after 223:")
r = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i mWakefulness="], capture_output=True, text=True)
print(r.stdout.strip())

time.sleep(1)
print("Testing wake up with input keyevent 224 (WAKEUP)...")
subprocess.run([adb, "-s", dev, "shell", "input keyevent 224"], check=True)
time.sleep(1)

print("Wakefulness after 224:")
r = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i mWakefulness="], capture_output=True, text=True)
print(r.stdout.strip())
