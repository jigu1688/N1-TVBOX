import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.111:5555'

subprocess.run([adb, 'connect', dev])
dumpsys = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys input'], capture_output=True, encoding='utf-8', errors='ignore').stdout

current_device = None
for line in dumpsys.splitlines():
    if 'Device ' in line:
        current_device = line.strip()
        print('\n' + current_device)
    elif current_device and any(k in line for k in ['Name:', 'Classes:', 'Path:', 'KeyLayoutFile:', 'KeyCharacterMapFile:', 'Sources:']):
        print('  ' + line.strip())
