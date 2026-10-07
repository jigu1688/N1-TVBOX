import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

subprocess.run([adb, 'connect', dev])

def sh(cmd):
    res = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, text=True)
    return res.stdout.strip()

print('=== Packages matching atv ===')
print(sh('pm list packages -f | grep atv'))

print('=== Find under /data/data/ca.dstudio.atvlauncher.pro ===')
print(sh('ls -laR /data/data/ca.dstudio.atvlauncher.pro'))

print('=== Database dir ===')
print(sh('ls -la /data/data/ca.dstudio.atvlauncher.pro/databases'))
