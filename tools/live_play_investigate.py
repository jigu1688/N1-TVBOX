import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

def run_adb(cmd, input_text=None):
    full_cmd = [adb, '-s', dev] + cmd
    return subprocess.run(full_cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', input=input_text).stdout

print("[*] 1. Connecting to ADB...", flush=True)
subprocess.run([adb, 'connect', dev], capture_output=True, text=True, encoding='utf-8', errors='ignore')

print("\n=== 2. CHECKING INSTALLED PACKAGES ===", flush=True)
pkgs = run_adb(['shell', 'pm list packages -f -u | grep -E "google|vending|gms"'])
print(pkgs)

print("\n=== 3. CHECKING DUMPSYS ACCOUNT ===", flush=True)
print(run_adb(['shell', 'dumpsys account']))

print("\n=== 4. CLEAR LOGCAT & LAUNCH PLAY STORE ===", flush=True)
run_adb(['logcat', '-c'])
# Launch Play Store
run_adb(['shell', 'monkey -p com.android.vending -c android.intent.category.LAUNCHER 1'])
time.sleep(3)

print("\n=== 5. TRIGGER CLICK / ENTER ON SIGN-IN BUTTON ===", flush=True)
run_adb(['shell', 'input keyevent 23']) # DPAD_CENTER
run_adb(['shell', 'input keyevent 66']) # ENTER
time.sleep(3)

print("\n=== 6. CAPTURED LOGCAT DURING CLICK ===", flush=True)
full_logs = run_adb(['logcat', '-d'])
lines = full_logs.splitlines()
print(f"Total logcat lines: {len(lines)}")
for l in lines[-120:]:
    print(l)

# Pull screenshot
run_adb(['shell', 'screencap -p /sdcard/play_click_debug.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/play_click_debug.png', 'tools/play_click_debug.png'], capture_output=True, text=True)
print("\n[+] Captured screen saved to tools/play_click_debug.png", flush=True)
