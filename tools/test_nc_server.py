import subprocess, time, socket

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("[*] Starting nc server on port 19999 on device...")
# Kill previous and run loop
server_cmd = """
pkill -f 'nc -l -p 19999'
sh -c 'while true; do /system/xbin/busybox nc -l -p 19999 -e /system/bin/input keyevent 223; done' >/dev/null 2>&1 &
"""
sh(server_cmd)
time.sleep(1)

print("[*] Checking port 19999 is listening:")
print(sh("netstat -an | grep 19999"))

print("[*] Current wakefulness before connect:", sh("dumpsys power | grep -i wakefulness"))

# Connect to device port 19999
print("[*] Connecting to port 19999...")
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(("192.168.31.118", 19999))
    s.sendall(b"sleep\n")
    s.close()
    print("    Socket triggered successfully!")
except Exception as e:
    print("    Socket error:", e)

time.sleep(1)
print("[*] Wakefulness after socket:", sh("dumpsys power | grep -i wakefulness"))

# Wake it back up
print("[*] Waking up back to Awake...")
sh("input keyevent 224")
print("[*] Restored wakefulness:", sh("dumpsys power | grep -i wakefulness"))
