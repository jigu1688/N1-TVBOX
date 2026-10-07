"""Verification: check all critical file SELinux labels in the built image"""
import struct, subprocess, re

img = 'build_rom/system.raw.img'

def get_inode(path):
    r = subprocess.run(['wsl', 'debugfs', '-R', f'stat {path}', img], capture_output=True, text=True)
    m = re.search(r'Inode:\s+(\d+)', r.stdout)
    return int(m.group(1)) if m else None

def check_xattr(inode_num, label, expected_label):
    with open(img, 'rb') as f:
        f.seek(1024)
        sb = f.read(1024)
        sipg = struct.unpack_from('<I', sb, 40)[0]
        isz = struct.unpack_from('<H', sb, 88)[0]
        bsz = 1024 << struct.unpack_from('<I', sb, 24)[0]
        
        bg = (inode_num - 1) // sipg
        idx = (inode_num - 1) % sipg
        f.seek(bsz + bg * 32)
        gd = f.read(32)
        itbl = struct.unpack_from('<I', gd, 8)[0]
        off = itbl * bsz + idx * isz
        f.seek(off)
        inode = f.read(isz)
        tail = inode[128:256]
        
        # Parse xattr value
        es = struct.unpack_from('<H', tail, 0)[0]  # extra_isize
        magic = struct.unpack_from('<I', tail, es)[0]
        if magic != 0xEA020000:
            print(f"  {label}: NO XATTR MAGIC (0x{magic:08X})")
            return False
        
        entry_off = es + 4
        vo = struct.unpack_from('<H', tail, entry_off + 2)[0]
        vs = struct.unpack_from('<I', tail, entry_off + 8)[0]
        val = tail[entry_off + vo:entry_off + vo + vs]
        val_str = val.rstrip(b'\x00').decode('ascii', errors='replace')
        
        ok = val_str == expected_label
        status = "OK" if ok else "BROKEN"
        print(f"  {label}: [{status}] label = '{val_str}' (expected: '{expected_label}')")
        return ok

expected_paths = [
    ('/bin/webpad', 'webpad', 'u:object_r:rootfs:s0'),
    ('/bin/webpadinit.sh', 'webpadinit.sh', 'u:object_r:rootfs:s0'),
    ('/xbin/daemonsu', 'daemonsu', 'u:object_r:rootfs:s0'),
    ('/xbin/busybox', 'busybox', 'u:object_r:system_file:s0'),
    ('/xbin/su', 'su', 'u:object_r:shell_exec:s0'),
    ('/xbin/supolicy', 'supolicy', 'u:object_r:shell_exec:s0'),
    ('/bin/do_sleep.sh', 'do_sleep.sh', 'u:object_r:system_file:s0'),
    ('/bin/run_nc.sh', 'run_nc.sh', 'u:object_r:system_file:s0'),
    ('/etc/init/daemonsu.rc', 'daemonsu.rc', 'u:object_r:system_file:s0'),
]

print("SELinux xattr verification for built image:")
all_ok = True
for path, label, expected_label in expected_paths:
    ino = get_inode(path)
    if ino:
        if not check_xattr(ino, f"{label} (inode {ino})", expected_label):
            all_ok = False
    else:
        print(f"  {label}: NOT FOUND in image")
        all_ok = False

print()
if all_ok:
    print("[+] ALL LABELS CORRECT! Webpad early-boot trust chain verified.")
else:
    print("[!] SOME LABELS ARE BROKEN!")
    exit(1)
