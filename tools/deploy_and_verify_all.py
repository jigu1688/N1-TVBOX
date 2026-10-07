import subprocess, os, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

print(f"[*] Connecting to {dev}...")
subprocess.run([adb, "connect", dev], check=True)
subprocess.run([adb, "-s", dev, "shell", "mount -o remount,rw /system"], check=True)

# 1. Push PhiTvSettings.apk
apk_local = os.path.abspath("build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk")
print(f"[*] Pushing latest PhiTvSettings.apk ({os.path.getsize(apk_local)} bytes)...")
subprocess.run([adb, "-s", dev, "push", apk_local, "/system/priv-app/PhiTvSettings/PhiTvSettings.apk"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 644 /system/priv-app/PhiTvSettings/PhiTvSettings.apk && chown 0:0 /system/priv-app/PhiTvSettings/PhiTvSettings.apk"], check=True)

# 2. Deploy run_nc.sh and install-recovery.sh
daemon_script = """#!/system/bin/sh
while true; do
    /system/xbin/busybox nc -l -p 19999 -e /system/bin/input keyevent 223
    sleep 0.1
done
"""
with open("tools/re_tools/run_nc.sh", "w", newline="\n") as f:
    f.write(daemon_script)
subprocess.run([adb, "-s", dev, "push", "tools/re_tools/run_nc.sh", "/system/bin/run_nc.sh"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 755 /system/bin/run_nc.sh && chown 0:0 /system/bin/run_nc.sh"], check=True)

recovery_script = """#!/system/bin/sh
/system/bin/run_nc.sh &
exit 0
"""
with open("tools/re_tools/install-recovery.sh", "w", newline="\n") as f:
    f.write(recovery_script)
subprocess.run([adb, "-s", dev, "push", "tools/re_tools/install-recovery.sh", "/system/bin/install-recovery.sh"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 755 /system/bin/install-recovery.sh && chown 0:0 /system/bin/install-recovery.sh"], check=True)

# Also sync both to build_rom
shutil_sync = """
import shutil
shutil.copy2('tools/re_tools/run_nc.sh', 'build_rom/system_root/bin/run_nc.sh')
shutil.copy2('tools/re_tools/install-recovery.sh', 'build_rom/system_root/bin/install-recovery.sh')
"""
subprocess.run(["python", "-c", shutil_sync], check=True)

# 3. Ensure run_nc.sh is running right now
subprocess.run([adb, "-s", dev, "shell", "pkill -f run_nc.sh; pkill -f 'nc -l -p 19999'; /system/bin/run_nc.sh >/dev/null 2>&1 &"])
time.sleep(1)

# Verify port 19999 is LISTEN
r_port = subprocess.run([adb, "-s", dev, "shell", "netstat -an | grep 19999"], capture_output=True, text=True)
print("    Port 19999 check:", r_port.stdout.strip())

# 4. Force stop tvsettings so it reloads fresh APK
subprocess.run([adb, "-s", dev, "shell", "am force-stop com.android.tv.settings"])

# 5. Test ShutdownActivity
print("\n[*] Starting ShutdownActivity to test countdown sleep...")
subprocess.run([adb, "-s", dev, "logcat", "-c"])
subprocess.run([adb, "-s", dev, "shell", "am start -n com.android.tv.settings/.ShutdownActivity"])

print("[*] Waiting 9 seconds for countdown to expire...")
time.sleep(9)

print("\n=== FINAL TEST RESULTS ===")
res_wake = subprocess.run([adb, "-s", dev, "shell", "dumpsys power | grep -i wakefulness"], capture_output=True, text=True)
wake_status = res_wake.stdout.strip()
print("Device Wakefulness:", wake_status)

r_log = subprocess.run([adb, "-s", dev, "logcat", "-d"], capture_output=True, text=True, errors="replace")
for l in r_log.stdout.splitlines():
    if any(k in l for k in ["SafeSleepManager", "ShutdownActivity"]):
        print("  ", l)

if "Asleep" in wake_status:
    print("\n[SUCCESS] BOX ENTERED ASLEEP LOW-POWER SLEEP STATE SUCCESSFULLY!")
    print("[*] Waking box back up so user can test via remote control...")
    subprocess.run([adb, "-s", dev, "shell", "input keyevent 224"])
else:
    print("\n[!] Still Awake. Please inspect log above.")
