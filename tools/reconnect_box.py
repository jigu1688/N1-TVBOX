import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

for i in range(10):
    res = subprocess.run([adb, 'connect', dev], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    print(f"Attempt {i+1}: {res.stdout.strip()}", flush=True)
    if 'connected to' in res.stdout:
        res2 = subprocess.run([adb, '-s', dev, 'shell', 'getprop sys.boot_completed'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print("boot_completed:", res2.stdout.strip(), flush=True)
        if res2.stdout.strip() == '1':
            break
    time.sleep(2)
