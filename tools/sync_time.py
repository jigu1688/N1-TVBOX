import datetime, subprocess

now = datetime.datetime.now()
print('Host Real Time:', now)

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Set ntp server to aliyun
subprocess.run([adb, '-s', dev, 'shell', 'settings', 'put', 'global', 'ntp_server', 'ntp.aliyun.com'])

# Format date for Android: YYYYMMDD.hhmmss
date_str = now.strftime('%Y%m%d.%H%M%S')
subprocess.run([adb, '-s', dev, 'shell', f'date -s {date_str}'])
res = subprocess.run([adb, '-s', dev, 'shell', 'date'], capture_output=True, text=True)
print('Device Date after sync:', res.stdout.strip())
