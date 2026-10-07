import subprocess
import time
import os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

time.sleep(3)
subprocess.run([adb, 'connect', dev], capture_output=True)

# Capture screenshot
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_restored.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_restored.png', 'tools/screen_restored.png'], capture_output=True)

dest = 'tools/screen_restored.png'
if os.path.exists(dest) and os.path.getsize(dest) > 1000:
    print(f"[+] SUCCESS: Screen captured! Size: {os.path.getsize(dest)} bytes")
else:
    print("[!] Failed to capture screen.")
