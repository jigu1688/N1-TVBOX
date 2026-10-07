import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd_args, timeout=10):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    full_cmd = [adb, '-s', dev] + cmd_args
    r = subprocess.run(full_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout, r.stderr

print("[*] 1. Clear logcat:")
run(['logcat', '-c'])

print("[*] 2. Launch ShutdownActivity:")
run(['shell', 'am start -n com.android.tv.settings/.ShutdownActivity'])

print("[*] 3. Waiting 9 seconds for countdown to expire and sleep...")
time.sleep(9)

print("[*] 4. Checking logcat:")
out, _ = run(['logcat', '-d'])
for line in out.splitlines():
    if any(k in line for k in ['SafeSleepManager', 'ShutdownActivity', 'goToSleep']):
        print("  ", line)

print("[*] 5. Checking mWakefulness:")
out, _ = run(['shell', 'dumpsys power | grep mWakefulness'])
print("   ", out.strip())
