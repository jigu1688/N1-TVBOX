import subprocess
import re

def get_inode(img_path, file_path):
    r = subprocess.run(['wsl', 'debugfs', '-R', f'stat {file_path}', img_path], capture_output=True, text=True)
    m = re.search(r'Inode:\s+(\d+)', r.stdout)
    if m:
        return int(m.group(1))
    return None

img = 'build_rom/system.raw.img'
for p in ['/bin/webpad', '/xbin/busybox', '/bin/do_sleep.sh', '/bin/run_nc.sh', '/bin/install-recovery.sh', '/xbin/su']:
    ino = get_inode(img, p)
    print(f"{p} -> inode {ino}")
