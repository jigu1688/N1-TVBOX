import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("[*] Setting up FIFO sleep helper on device...")
setup_cmd = """
rm -f /data/local/tmp/sleep_fifo
mknod /data/local/tmp/sleep_fifo p 2>/dev/null || mkfifo /data/local/tmp/sleep_fifo
chmod 666 /data/local/tmp/sleep_fifo

# Start background listener in subshell
sh -c 'while true; do read line < /data/local/tmp/sleep_fifo; if [ "$line" = "sleep" ]; then /system/bin/input keyevent 223; fi; done' >/dev/null 2>&1 &
"""
sh(setup_cmd)

print("[*] Checking FIFO exists:")
print(sh("ls -l /data/local/tmp/sleep_fifo"))

print("[*] Current wakefulness before writing FIFO:", sh("dumpsys power | grep -i wakefulness"))

print("[*] Simulating app writing 'sleep' to FIFO...")
sh("echo sleep > /data/local/tmp/sleep_fifo")

time.sleep(1)
print("[*] Wakefulness after writing FIFO:", sh("dumpsys power | grep -i wakefulness"))

# Wake it back up
time.sleep(1)
print("[*] Waking back up...")
sh("input keyevent 224")
print("[*] Restored wakefulness:", sh("dumpsys power | grep -i wakefulness"))
