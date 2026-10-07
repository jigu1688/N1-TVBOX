import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

res_pm = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d | grep -i gmscore'], capture_output=True, text=True, errors='ignore')
print('GmsCore logcat records:\n', res_pm.stdout)

res_err = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d | grep -i "failed to parse"'], capture_output=True, text=True, errors='ignore')
print('Failed to parse records:\n', res_err.stdout)
