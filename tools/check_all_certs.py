import os, subprocess

apksigner = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat'
gms_clean = 'tools/gms_system_clean'

print('=== CHECKING SIGNATURES IN gms_system_clean ===')
for root, dirs, files in os.walk(gms_clean):
    for f in files:
        if f.endswith('.apk'):
            p = os.path.join(root, f)
            res = subprocess.run(f'{apksigner} verify --print-certs "{p}"', shell=True, capture_output=True, text=True, errors='ignore')
            print('-----------------------------------------')
            print('File:', f, f'({os.path.getsize(p)/1024/1024:.2f} MB)')
            for line in res.stdout.splitlines():
                if any(k in line for k in ['Signer', 'Subject', 'SHA-256', 'MD5']):
                    print('  ', line)
            if res.returncode != 0:
                print('   ERROR:', res.stderr)
