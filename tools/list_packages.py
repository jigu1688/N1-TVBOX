import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

r = subprocess.run([adb, '-s', dev, 'shell', 'pm list packages'], capture_output=True, text=True)
all_pkgs = sorted(r.stdout.strip().split('\n'))

print('=== Installed Packages on Device ===')
for p in all_pkgs:
    p = p.replace('package:', '').strip()
    if any(k in p.lower() for k in ['kodi', 'hpplay', 'video', 'webpush', 'file', 'setting', 'atv', 'launcher', 'media', 'music', 'nas', 'browser']):
        print('  [Relevant]', p)
    elif not p.startswith('com.android.') and not p.startswith('android'):
        print('  [Other]', p)
