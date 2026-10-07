import os, subprocess

aapt = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\aapt.exe'
gms_clean = 'tools/gms_system_clean'

print('=== INSPECTING AAPT BADGING FOR ALL GMS APKS ===')
for root, dirs, files in os.walk(gms_clean):
    for f in files:
        if f.endswith('.apk'):
            p = os.path.join(root, f)
            res = subprocess.run([aapt, 'dump', 'badging', p], capture_output=True, text=True, errors='ignore')
            first_line = res.stdout.splitlines()[0] if res.stdout else "ERROR"
            shared_user = ""
            for line in res.stdout.splitlines():
                if 'sharedUserId' in line:
                    shared_user = line
            print('-----------------------------------------')
            print(f"File: {f}")
            print(f"  {first_line}")
            if shared_user:
                print(f"  {shared_user}")
