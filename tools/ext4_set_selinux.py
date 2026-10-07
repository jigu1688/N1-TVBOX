import os
import re
import struct
import subprocess

EXT4_XATTR_MAGIC = 0xEA020000

# 128-byte block representing standard ext4 inode extra region (extra_isize=28) + SELinux xattr:
# security.selinux = "u:object_r:system_file:s0\0"
SELINUX_SYSTEM_FILE_TAIL = bytes.fromhex(
    '1c000000000000000000000000000000000000000000000000000000000002ea'
    '07064000000000001a0000000000000073656c696e7578000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000'
    '753a6f626a6563745f723a73797374656d5f66696c653a733000000000000000'
)

# security.selinux = "u:object_r:rootfs:s0\0"
# CRITICAL: init only allows transition to adbd on rootfs-labeled files
SELINUX_ROOTFS_TAIL = bytes.fromhex(
    '1c000000000000000000000000000000000000000000000000000000000002ea'
    '0706440000000000150000000000000073656c696e7578000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000'
    '00000000753a6f626a6563745f723a726f6f7466733a73300000000000000000'
)

# security.selinux = "u:object_r:shell_exec:s0\0"
SELINUX_SHELL_EXEC_TAIL = bytes.fromhex(
    '1c000000000000000000000000000000000000000000000000000000000002ea'
    '0706400000000000190000000000000073656c696e7578000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000'
    '753a6f626a6563745f723a7368656c6c5f657865633a73300000000000000000'
)

# Rootfs paths: must be u:object_r:rootfs:s0 so init can launch webpadservice under adbd
ROOTFS_PATHS = [
    '/bin/webpad',
    '/bin/webpadinit.sh',
    '/xbin/daemonsu'
]

# Shell exec paths
SHELL_EXEC_PATHS = [
    '/xbin/su',
    '/xbin/supolicy'
]

# System file paths: must be u:object_r:system_file:s0
SYSTEM_FILE_PATHS = [
    '/xbin/busybox',
    '/bin/do_sleep.sh',
    '/bin/run_nc.sh',
    '/bin/install-recovery.sh',
    '/etc/init/daemonsu.rc'
]

def get_inode_num(img_path, file_path):
    r = subprocess.run(['wsl', 'debugfs', '-R', f'stat {file_path}', img_path], capture_output=True, text=True)
    m = re.search(r'Inode:\s+(\d+)', r.stdout)
    if m:
        return int(m.group(1))
    return None

def set_inode_tail(f, inode_num, tail_bytes, s_inodes_per_group, s_inode_size, block_size):
    bg = (inode_num - 1) // s_inodes_per_group
    idx = (inode_num - 1) % s_inodes_per_group

    f.seek(block_size + bg * 32)
    gd = f.read(32)
    bg_inode_table = struct.unpack_from('<I', gd, 8)[0]

    offset = bg_inode_table * block_size + idx * s_inode_size + 128
    f.seek(offset)
    f.write(tail_bytes)

def fix_all_selinux_in_image(img_path):
    print(f"[*] Scanning and enforcing SELinux labels in {img_path}...")
    fixed_count = 0
    total_inodes = 0

    with open(img_path, 'r+b') as f:
        f.seek(1024)
        sb = f.read(1024)
        s_inodes_count = struct.unpack_from('<I', sb, 0)[0]
        s_log_block_size = struct.unpack_from('<I', sb, 24)[0]
        s_inodes_per_group = struct.unpack_from('<I', sb, 40)[0]
        s_inode_size = struct.unpack_from('<H', sb, 88)[0]
        s_desc_size = struct.unpack_from('<H', sb, 254)[0] if struct.unpack_from('<H', sb, 96)[0] & 0x80 else 32
        if s_desc_size < 32: s_desc_size = 32

        block_size = 1024 << s_log_block_size
        num_groups = (s_inodes_count + s_inodes_per_group - 1) // s_inodes_per_group
        gd_table_block = 1 if block_size > 1024 else 2

        for bg in range(num_groups):
            gd_offset = gd_table_block * block_size + bg * s_desc_size
            f.seek(gd_offset)
            gd = f.read(s_desc_size)
            bg_inode_bitmap = struct.unpack_from('<I', gd, 4)[0]
            bg_inode_table = struct.unpack_from('<I', gd, 8)[0]

            f.seek(bg_inode_bitmap * block_size)
            bitmap_len = (s_inodes_per_group + 7) // 8
            bitmap = f.read(bitmap_len)

            for idx in range(s_inodes_per_group):
                inode_num = bg * s_inodes_per_group + idx + 1
                if inode_num > s_inodes_count: break
                
                byte_idx = idx // 8
                bit_idx = idx % 8
                if not (bitmap[byte_idx] & (1 << bit_idx)):
                    continue

                inode_offset = bg_inode_table * block_size + idx * s_inode_size
                f.seek(inode_offset)
                inode_data = bytearray(f.read(s_inode_size))
                
                i_mode = struct.unpack_from('<H', inode_data, 0)[0]
                if i_mode == 0: continue
                total_inodes += 1

                extra_isize = struct.unpack_from('<H', inode_data, 128)[0]
                xattr_magic = struct.unpack_from('<I', inode_data, 156)[0] if len(inode_data) >= 160 else 0

                # Check if it already has valid SELinux label
                if extra_isize != 28 or xattr_magic != EXT4_XATTR_MAGIC:
                    inode_data[128:256] = SELINUX_SYSTEM_FILE_TAIL
                    f.seek(inode_offset)
                    f.write(inode_data)
                    fixed_count += 1

        # 1. Enforce rootfs on webpad and boot components
        for path in ROOTFS_PATHS:
            ino = get_inode_num(img_path, path)
            if ino:
                set_inode_tail(f, ino, SELINUX_ROOTFS_TAIL, s_inodes_per_group, s_inode_size, block_size)
                print(f"  [+] Enforced u:object_r:rootfs:s0 on {path} (inode {ino})")

        # 2. Enforce shell_exec on su and supolicy
        for path in SHELL_EXEC_PATHS:
            ino = get_inode_num(img_path, path)
            if ino:
                set_inode_tail(f, ino, SELINUX_SHELL_EXEC_TAIL, s_inodes_per_group, s_inode_size, block_size)
                print(f"  [+] Enforced u:object_r:shell_exec:s0 on {path} (inode {ino})")

        # 3. Enforce system_file on system binaries & scripts
        for path in SYSTEM_FILE_PATHS:
            ino = get_inode_num(img_path, path)
            if ino:
                set_inode_tail(f, ino, SELINUX_SYSTEM_FILE_TAIL, s_inodes_per_group, s_inode_size, block_size)
                print(f"  [+] Enforced u:object_r:system_file:s0 on {path} (inode {ino})")

        f.flush()
    print(f"[+] Scan complete: {total_inodes} allocated inodes checked, {fixed_count} unlabeled inodes repaired with standard SELinux security context!")

if __name__ == '__main__':
    fix_all_selinux_in_image('build_rom/system.raw.img')
    res = subprocess.run(['wsl', 'e2fsck', '-f', '-n', 'build_rom/system.raw.img'], capture_output=True, text=True)
    print(res.stdout)
