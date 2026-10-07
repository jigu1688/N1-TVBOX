import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

res = subprocess.run([adb, '-s', dev, 'shell', 'dumpsys package | grep -E "(Package \[|signatures:)"'], capture_output=True, text=True, errors='ignore')
lines = res.stdout.splitlines()

for i in range(len(lines)):
    if 'Package [' in lines[i]:
        pkg = lines[i].strip()
        if any(k in pkg for k in ['google', 'vending', 'gms', 'android']):
            print(pkg)
            for j in range(i+1, min(i+10, len(lines))):
                if 'signatures:' in lines[j] or 'PackageSignatures' in lines[j] or 'Signing Package:' in lines[j]:
                    print("  ", lines[j].strip())
                if 'Package [' in lines[j]:
                    break
