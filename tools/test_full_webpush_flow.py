import subprocess, time, urllib.request

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'
subprocess.run([adb, 'connect', dev])

print('=== UNINSTALLING SeleneTV ===')
subprocess.run([adb, '-s', dev, 'shell', 'pm uninstall org.moontechlab.selenetv'])
time.sleep(1)

print('=== VERIFY UNINSTALLED ===')
r = subprocess.run([adb, '-s', dev, 'shell', 'pm path org.moontechlab.selenetv'], capture_output=True, text=True)
print('Path after uninstall:', r.stdout.strip())

print('=== TRIGGER WEBPUSH INSTALL API ===')
payload = b'{"fileName":"SeleneTV-v1.4.6-arm64-v8a.apk"}'
req = urllib.request.Request(
    'http://192.168.31.115:8888/api/install',
    data=payload,
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=15)
print('WebPush response:', resp.read().decode('utf-8'))

time.sleep(2)
print('=== VERIFY REINSTALLED ===')
r2 = subprocess.run([adb, '-s', dev, 'shell', 'pm path org.moontechlab.selenetv'], capture_output=True, text=True)
print('Path after WebPush install:', r2.stdout.strip())
