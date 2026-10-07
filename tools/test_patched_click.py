import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

def run_adb(cmd):
    full_cmd = [adb, '-s', dev] + cmd
    return subprocess.run(full_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore').stdout

print("[*] 1. Reconnecting to device...", flush=True)
for i in range(10):
    res = subprocess.run([adb, 'connect', dev], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(f"  Attempt {i+1}: {res.stdout.strip()}", flush=True)
    if 'connected to' in res.stdout:
        break
    time.sleep(2)

print("\n[*] 2. Checking GmsCore status on device...", flush=True)
print(run_adb(['shell', 'pm path com.google.android.gms']))
print(run_adb(['shell', 'dumpsys account | grep -E "Authenticator|com.google"']))

print("\n[*] 3. Clearing logcat and launching Play Store...", flush=True)
run_adb(['logcat', '-c'])
run_adb(['shell', 'monkey -p com.android.vending -c android.intent.category.LAUNCHER 1'])
time.sleep(3)

print("\n[*] 4. Triggering click on Sign-in button...", flush=True)
run_adb(['shell', 'input keyevent 23'])
time.sleep(1)
run_adb(['shell', 'input keyevent 66'])
time.sleep(3)

print("\n[*] 5. Dumping relevant logs...", flush=True)
logs = run_adb(['logcat', '-d'])
matches = []
for line in logs.splitlines():
    if any(k in line.lower() for k in ['authenticator', 'securityexception', 'cannot delegate', 'finsky', 'vending', 'activitymanager', 'addaccount', 'uath']):
        matches.append(line)

print(f"Total matching lines: {len(matches)}")
for m in matches[-50:]:
    print(" ", m)

# Screencap
run_adb(['shell', 'screencap -p /sdcard/play_patched_result.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/play_patched_result.png', 'tools/play_patched_result.png'])
print("\n[+] Pull screenshot to tools/play_patched_result.png", flush=True)
