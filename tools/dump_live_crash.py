import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# 1. Capture recent crash logs
r = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d -t 150 *:E'], capture_output=True, text=True)
print("=== LOGCAT ERRORS ===")
print(r.stdout)

# 2. Capture specific crash stack traces
r2 = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d -s AndroidRuntime:E'], capture_output=True, text=True)
print("=== ANDROID RUNTIME CRASHES ===")
print(r2.stdout[-3000:])
