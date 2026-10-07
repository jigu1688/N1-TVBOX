import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])

def sh(cmd):
    res = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, encoding='utf-8', errors='ignore')
    return res.stdout

print('=== LS -LAZ /system/usr/keylayout ===')
print(sh('ls -laZ /system/usr/keylayout/Generic.kl /system/usr/keylayout/Vendor_0001_Product_0001.kl'))

print('=== LOGCAT EventHub / KeyLayout ===')
logcat = sh('logcat -d | grep -iE "keylayout|eventhub|keycharacter"')
print(logcat[:3000])
