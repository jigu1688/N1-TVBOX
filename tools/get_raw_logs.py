import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

subprocess.run([adb, 'connect', dev], capture_output=True)

# Fetch last 200 lines from logcat
p = subprocess.run([adb, '-s', dev, 'shell', 'logcat -d | tail -n 200'], capture_output=True)
lines = p.stdout.decode('utf-8', errors='ignore').splitlines()

print(f"Total lines captured: {len(lines)}")
for line in lines[-60:]:
    print(line)
