import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("[*] Creating FIFO at /dev/sleep_fifo...")
sh("rm -f /dev/sleep_fifo && mkfifo /dev/sleep_fifo && chmod 666 /dev/sleep_fifo")

# Background listener on /dev/sleep_fifo
sh("sh -c 'while true; do read l < /dev/sleep_fifo; if [ \"$l\" = \"sleep\" ]; then /system/bin/input keyevent 223; fi; done' >/dev/null 2>&1 &")

# Also start socket listener on 19999
sh("sh -c 'while true; do /system/xbin/busybox nc -l -p 19999 -e /system/bin/input keyevent 223; done' >/dev/null 2>&1 &")

print("[*] /dev/sleep_fifo permissions:")
print(sh("ls -l /dev/sleep_fifo"))

print("[*] Current wakefulness before write:", sh("dumpsys power | grep -i wakefulness"))

# Simulate writing sleep to /dev/sleep_fifo
sh("echo sleep > /dev/sleep_fifo")
time.sleep(1)

print("[*] Wakefulness after writing to /dev/sleep_fifo:", sh("dumpsys power | grep -i wakefulness"))

# Wake it back up
sh("input keyevent 224")
print("[*] Restored wakefulness:", sh("dumpsys power | grep -i wakefulness"))
