import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])
dumpsys = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys input'], capture_output=True, encoding='utf-8', errors='ignore').stdout

start = dumpsys.find('Event Hub State:')
end = dumpsys.find('Input Reader State:')
if start != -1 and end != -1:
    print(dumpsys[start:end])
else:
    print(dumpsys[:4000])
