import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
r = subprocess.run([adb, '-s', dev, 'shell', 'strings /file_contexts.bin'], capture_output=True, text=True)

for line in r.stdout.splitlines():
    if any(k in line for k in ['recovery', 'daemonsu', 'webpad', 'adbd', 'su_exec']):
        print(line)
