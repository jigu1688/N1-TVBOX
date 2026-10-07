import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])

def sh(cmd):
    res = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, encoding='utf-8', errors='ignore')
    return res.stdout

print('=== GETEVENT -p ===')
print(sh('getevent -p'))

print('=== DUMPSYS INPUT (Event Hub Devices) ===')
dumpsys = sh('dumpsys input')
lines = dumpsys.splitlines()
for i, line in enumerate(lines):
    if 'Device ' in line or 'KeyLayoutFile:' in line or 'KeyCharacterMapFile:' in line or 'Classes:' in line:
        print(line)

print('\n=== LS -L /system/usr/keylayout ===')
print(sh('ls -l /system/usr/keylayout/Generic.kl /system/usr/keylayout/Vendor_0001_Product_0001.kl'))

print('\n=== BLUETOOTH DEVICES CONNECTED ===')
print(sh('dumpsys bluetooth_manager'))
