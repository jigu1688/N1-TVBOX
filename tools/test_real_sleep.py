import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("[*] Before sleep wakefulness:", sh("dumpsys power | grep -i wakefulness"))

# Let's test writeSysfs via binder to /sys/power/state
print("[*] Calling system_control writeSysfs /sys/power/state mem...")
r = subprocess.run([adb, "-s", dev, "shell", "service call system_control 2 s16 '/sys/power/state' s16 'mem'"], capture_output=True, text=True)
print("    Result:", r.stdout.strip())

time.sleep(2)
print("[*] Checking status after 2 seconds...")
r2 = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i wakefulness"], capture_output=True, text=True, timeout=3)
print("    Wakefulness:", r2.stdout.strip())
