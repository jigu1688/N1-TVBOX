import subprocess, time, socket

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("[*] Starting nc loop on port 19999...")
# Run via nohup or background script
daemon_script = """#!/system/bin/sh
while true; do
    /system/xbin/busybox nc -l -p 19999 -e /system/bin/input keyevent 223
    sleep 0.1
done
"""
subprocess.run([adb, "-s", dev, "shell", "mount -o remount,rw /system"], check=True)
with open("tools/re_tools/run_nc.sh", "w", newline="\n") as f:
    f.write(daemon_script)
subprocess.run([adb, "-s", dev, "push", "tools/re_tools/run_nc.sh", "/system/bin/run_nc.sh"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 755 /system/bin/run_nc.sh && chown 0:0 /system/bin/run_nc.sh"], check=True)

# Kill any existing and start run_nc.sh
sh("pkill -f run_nc.sh; pkill -f 'nc -l -p 19999'")
sh("/system/bin/run_nc.sh >/dev/null 2>&1 &")

time.sleep(1)
print("[*] Netstat check on device:")
print(sh("netstat -an | grep 19999"))

print("[*] Current wakefulness before socket:", sh("dumpsys power | grep -i wakefulness"))

# Now send a test packet to 192.168.31.118:19999
print("[*] Connecting from Python to port 19999...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(("192.168.31.118", 19999))
    s.sendall(b"sleep\n")
    s.close()
    print("[+] Sent sleep to port 19999 successfully!")
except Exception as e:
    print("[!] Connect failed:", e)

time.sleep(1)
print("[*] Wakefulness after socket:", sh("dumpsys power | grep -i wakefulness"))

# Wake it back up
sh("input keyevent 224")
print("[*] Restored wakefulness:", sh("dumpsys power | grep -i wakefulness"))
