import subprocess, re

paths = [
    '/bin/webpad',
    '/bin/webpadinit.sh',
    '/bin/install-recovery.sh',
    '/xbin/busybox',
    '/xbin/su',
    '/xbin/daemonsu',
    '/xbin/supolicy',
    '/etc/init/daemonsu.rc',
    '/bin/sh'
]

for p in paths:
    r = subprocess.run(['wsl', 'debugfs', '-R', f'stat {p}', 'extracted_webpad/system.raw.img'], capture_output=True, text=True)
    m = re.search(r'security\.selinux.*?=\s*\"([^\"]+)\"', r.stdout)
    if m:
        val = m.group(1).replace('\\000', '')
        print(f"{p:26}: {val}")
    else:
        # Check if file exists
        if 'File not found' in r.stdout:
            print(f"{p:26}: FILE NOT FOUND")
        else:
            print(f"{p:26}: NO XATTR (unlabeled)")
