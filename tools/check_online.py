import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

# Check if device is back online (user might have pressed remote)
r = subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
print("Connect:", r.stdout)

r2 = subprocess.run([adb, '-s', dev, 'shell', 'echo online'], capture_output=True, text=True)
print("Shell check:", r2.stdout, r2.stderr)
