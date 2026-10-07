import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"
subprocess.run([adb, "connect", dev], capture_output=True, timeout=5)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace", timeout=10).stdout.strip()

print("[*] Clearing logcat...")
subprocess.run([adb, "-s", dev, "logcat", "-c"])

print("[*] Starting ShutdownActivity...")
subprocess.run([adb, "-s", dev, "shell", "am start -n com.android.tv.settings/.ShutdownActivity"])

print("[*] Waiting 9 seconds for countdown to finish...")
time.sleep(9)

print("[*] Fetching logcat related to SafeSleepManager and PowerManager...")
r = subprocess.run([adb, "-s", dev, "logcat", "-d"], capture_output=True, text=True, errors="replace")
for line in r.stdout.splitlines():
    if any(k in line for k in ["SafeSleepManager", "ShutdownActivity", "goToSleep", "system_control", "writeSysfs"]):
        print(line)

print("[*] Current wakefulness:")
print(sh("dumpsys power | grep -i wakefulness"))
