import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])
dumpsys = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys input'], capture_output=True, encoding='utf-8', errors='ignore').stdout

for chunk in dumpsys.split('Device '):
    if any(k in chunk for k in ['遥控器', '2.4G', 'Generic.kl', 'Vendor_']):
        print('=== Device ' + chunk[:1500])
