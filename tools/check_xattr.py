import struct, subprocess, re

img = 'build_rom/system.raw.img'

def get_inode_num(path):
    r = subprocess.run(['wsl', 'debugfs', '-R', f'stat {path}', img], capture_output=True, text=True)
    m = re.search(r'Inode:\s+(\d+)', r.stdout)
    return int(m.group(1)) if m else None

ino = get_inode_num('/xbin/busybox')
su_ino = get_inode_num('/xbin/su')
print(f'Busybox inode: {ino}')
print(f'Su inode: {su_ino}')

with open(img, 'rb') as f:
    f.seek(1024)
    sb = f.read(1024)
    s_inodes_per_group = struct.unpack_from('<I', sb, 40)[0]
    s_inode_size = struct.unpack_from('<H', sb, 88)[0]
    block_size = 1024 << struct.unpack_from('<I', sb, 24)[0]
    
    def dump_inode_xattr(inode_num, label):
        bg = (inode_num - 1) // s_inodes_per_group
        idx = (inode_num - 1) % s_inodes_per_group
        gd_offset = block_size + bg * 32
        f.seek(gd_offset)
        gd = f.read(32)
        bg_inode_table = struct.unpack_from('<I', gd, 8)[0]
        inode_offset = bg_inode_table * block_size + idx * s_inode_size
        f.seek(inode_offset)
        inode = f.read(s_inode_size)
        tail = inode[128:256]
        
        print(f'\n=== {label} inode {inode_num} at offset {inode_offset} ===')
        for i in range(0, len(tail), 16):
            hex_str = ' '.join(f'{b:02x}' for b in tail[i:i+16])
            ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in tail[i:i+16])
            print(f'  {128+i:3d}: {hex_str:<48s} {ascii_str}')
        
        extra_isize = struct.unpack_from('<H', tail, 0)[0]
        print(f'extra_isize: {extra_isize}')
        xattr_magic = struct.unpack_from('<I', tail, extra_isize)[0]
        print(f'xattr magic: 0x{xattr_magic:08X}')
        
        if xattr_magic == 0xEA020000:
            es = extra_isize + 4
            ni = tail[es]
            nl = tail[es+1]
            vo = struct.unpack_from('<H', tail, es+2)[0]
            vi = struct.unpack_from('<I', tail, es+4)[0]
            vs = struct.unpack_from('<I', tail, es+8)[0]
            vh = struct.unpack_from('<I', tail, es+12)[0]
            nm = tail[es+16:es+16+nl]
            print(f'Entry: name_index={ni}, name_len={nl}, value_offs={vo}')
            print(f'  value_inum={vi}, value_size={vs}, hash=0x{vh:08X}')
            print(f'  name: {nm!r}')
            vabs = es + vo
            val = tail[vabs:vabs+vs]
            print(f'  value at tail[{vabs}]: {val!r}')
        
        # Check i_file_acl (external xattr block)
        i_file_acl = struct.unpack_from('<I', inode, 104)[0]
        print(f'i_file_acl (external xattr block): {i_file_acl}')
    
    dump_inode_xattr(ino, 'BUSYBOX')
    if su_ino:
        dump_inode_xattr(su_ino, 'SU')
