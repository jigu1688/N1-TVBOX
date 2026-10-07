import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

FLAG_DIR = "/data/data/com.android.tv.settings/files"
FLAG_FILE = f"{FLAG_DIR}/trigger_sleep"

sh(f"mkdir -p {FLAG_DIR} && chmod 777 {FLAG_DIR}")
sh(f"rm -f {FLAG_FILE}")

# Start background file watcher daemon
daemon_cmd = f"""
pkill -f 'sleep_daemon'
sh -c 'while true; do
    if [ -f {FLAG_FILE} ]; then
        rm -f {FLAG_FILE}
        /system/bin/input keyevent 223
    fi
    sleep 0.2
done' >/dev/null 2>&1 &
"""
sh(daemon_cmd)

print("[*] Current wakefulness before creating flag:", sh("dumpsys power | grep -i wakefulness"))

# Simulate creating flag file as uid 10010 (or touching it)
print("[*] Creating trigger_sleep flag...")
sh(f"touch {FLAG_FILE}")

time.sleep(0.8)
print("[*] Wakefulness after creating flag:", sh("dumpsys power | grep -i wakefulness"))

# Wake it back up
print("[*] Waking box back up...")
sh("input keyevent 224")
print("[*] Restored wakefulness:", sh("dumpsys power | grep -i wakefulness"))
