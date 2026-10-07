import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

print("[*] Clearing logcat...")
subprocess.run([adb, "-s", dev, "logcat", "-c"])

print("[*] Starting ShutdownActivity...")
subprocess.run([adb, "-s", dev, "shell", "am start -n com.android.tv.settings/.ShutdownActivity"])

print("[*] Monitoring countdown and what happens after 8 seconds...")
for sec in range(1, 12):
    time.sleep(1)
    focus = subprocess.run([adb, "-s", dev, "shell", "dumpsys window | grep -i mCurrentFocus"], capture_output=True, text=True).stdout.strip()
    wake = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i wakefulness"], capture_output=True, text=True).stdout.strip()
    print(f"  Sec {sec:2d}: {wake} | {focus}")

print("\n[*] Fetching relevant logs...")
r_log = subprocess.run([adb, "-s", dev, "logcat", "-d"], capture_output=True, text=True, errors="replace")
for l in r_log.stdout.splitlines():
    if any(k in l for k in ["SafeSleepManager", "ShutdownActivity", "Force finishing", "fatal"]):
        print("  ", l)
