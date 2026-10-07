import urllib.request, subprocess, os

# Try downloading from microG official repo
url = 'https://microg.org/fdroid/repo/com.google.android.gms_240913008.apk'
dest_apk = 'tools/microg_gmscore.apk'

print('[*] Downloading MicroG GmsCore from microg.org repo...')
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=30) as resp, open(dest_apk, 'wb') as f:
        f.write(resp.read())
    print(f'[+] Downloaded MicroG GmsCore: {os.path.getsize(dest_apk) / 1024 / 1024:.2f} MB')
except Exception as e:
    print('[!] Direct repo failed, trying alternate URL...', e)
    alt_url = 'https://github.com/microg/GmsCore/releases/download/v0.2.27.223616/com.google.android.gms-223616045.apk'
    req_alt = urllib.request.Request(alt_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_alt, timeout=30) as resp, open(dest_apk, 'wb') as f:
        f.write(resp.read())
    print(f'[+] Downloaded Alt GmsCore: {os.path.getsize(dest_apk) / 1024 / 1024:.2f} MB')

# Test install on live device
adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '10.0.0.102:5555'

print('[*] Installing GmsCore on live device 10.0.0.102:5555...')
res_inst = subprocess.run([adb, '-s', dev, 'install', '-r', '-d', dest_apk], capture_output=True, text=True)
print('Install output:\n', res_inst.stdout, res_inst.stderr)
