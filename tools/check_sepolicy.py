import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

subprocess.run([adb, 'connect', dev])
r = subprocess.run([adb, '-s', dev, 'shell', 'strings /sepolicy'], capture_output=True, text=True)

types = set()
for line in r.stdout.splitlines():
    if line.endswith('_exec'):
        types.add(line)

print("Found exec types in /sepolicy:")
for t in sorted(types):
    print(" ", t)
