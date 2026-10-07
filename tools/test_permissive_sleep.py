import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("[*] Setting supolicy permissive priv_app...")
print("supolicy result:", sh("/system/xbin/supolicy --live 'permissive priv_app;'"))

# Test if tvsettings (uid 10010) can write to /data/local/tmp/sleep_fifo
print("[*] Testing run-as / permission check on FIFO:")
sh("rm -f /data/local/tmp/sleep_fifo && mkfifo /data/local/tmp/sleep_fifo && chmod 666 /data/local/tmp/sleep_fifo")

# Start background reader
sh("sh -c 'while true; do read l < /data/local/tmp/sleep_fifo; if [ \"$l\" = \"sleep\" ]; then /system/bin/input keyevent 223; fi; done' >/dev/null 2>&1 &")

# Trigger ShutdownActivity
print("[*] Clearing logcat and starting ShutdownActivity...")
subprocess.run([adb, "-s", dev, "logcat", "-c"])
subprocess.run([adb, "-s", dev, "shell", "am start -n com.android.tv.settings/.ShutdownActivity"])

print("[*] Waiting 9 seconds for countdown to finish...")
time.sleep(9)

print("\n=== RESULTS ===")
wake = sh("dumpsys power | grep -i wakefulness")
print("Wakefulness:", wake)

r_log = subprocess.run([adb, "-s", dev, "logcat", "-d"], capture_output=True, text=True, errors="replace")
for l in r_log.stdout.splitlines():
    if any(k in l for k in ["SafeSleepManager", "ShutdownActivity"]):
        print("  ", l)

if "Asleep" in wake:
    print("\n[SUCCESS] DEVICE ENTERED ASLEEP STANDBY SAFELY!")
    # Wake back up
    sh("input keyevent 224")
