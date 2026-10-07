import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

for pkg in ['android', 'com.google.android.gms', 'com.google.android.gsf', 'com.google.android.gsf.login', 'com.android.vending']:
    res = subprocess.run([adb, '-s', dev, 'shell', f'dumpsys package {pkg}'], capture_output=True, text=True, errors='ignore')
    print(f"=== {pkg} ===")
    for line in res.stdout.splitlines():
        if any(k in line for k in ['signatures:', 'PackageSignatures', 'sharedUserId', 'userId=', 'versionCode=']):
            print(" ", line.strip())
