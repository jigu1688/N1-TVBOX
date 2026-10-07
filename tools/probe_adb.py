import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'

for ip in ['10.0.0.100', '10.0.0.102', '10.0.0.103', '10.0.0.104']:
    p = subprocess.run([adb, 'connect', f'{ip}:5555'], capture_output=True)
    out = p.stdout.decode('utf-8', errors='ignore').strip()
    print(f"{ip}: {out}")

p_dev = subprocess.run([adb, 'devices'], capture_output=True)
print("\nDevices:\n" + p_dev.stdout.decode('utf-8', errors='ignore'))
