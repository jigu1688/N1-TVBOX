import struct

# Construct the correct 128-byte SELINUX_SU_EXEC_TAIL
# Must match the SU inode's xattr structure exactly
tail = bytearray(128)

# extra_isize = 28
struct.pack_into('<H', tail, 0, 28)
# bytes 2-27: padding (zeros)

# xattr magic at offset 28
struct.pack_into('<I', tail, 28, 0xEA020000)

# xattr entry at offset 32
entry_start = 32
tail[entry_start] = 7       # e_name_index = XATTR_INDEX_SECURITY
tail[entry_start+1] = 6     # e_name_len = 6 (length of "selinu" - the 'x' is at position 7 but name_len=6 matches original)
struct.pack_into('<H', tail, entry_start+2, 68)   # e_value_offs = 68
struct.pack_into('<I', tail, entry_start+4, 0)     # e_value_inum = 0
struct.pack_into('<I', tail, entry_start+8, 22)    # e_value_size = 22
struct.pack_into('<I', tail, entry_start+12, 0)    # e_hash = 0

# name at offset 48 (entry_start + 16), 7 bytes "selinux" + null padding
tail[48:48+7] = b'selinux'

# value at offset 100 (entry_start + e_value_offs = 32 + 68 = 100)
value = b'u:object_r:su_exec:s0\x00'
tail[100:100+22] = value

hex_str = tail.hex()
print("Correct SELINUX_SU_EXEC_TAIL hex dump:")
for i in range(0, 128, 16):
    h = ' '.join('{:02x}'.format(tail[i+j]) for j in range(16))
    a = ''.join(chr(tail[i+j]) if 32 <= tail[i+j] < 127 else '.' for j in range(16))
    print("  {:3d}: {}  {}".format(128+i, h, a))

print()
print("Python hex constant (4 lines of 32 bytes each):")
for i in range(0, len(hex_str), 64):
    print("    '{}'".format(hex_str[i:i+64]))

print()
print("Total length: {} bytes".format(len(tail)))

# Verify it matches the SU inode structure from the image
su_hex = (
    '1c000000000000000000000000000000000000000000000000000000000002ea'
    '0706440000000000160000000000000073656c696e7578000000000000000000'
    '0000000000000000000000000000000000000000000000000000000000000000'
    '0000000075 3a6f626a6563745f723a73755f657865633a733000000000000000'
).replace(' ', '')

print()
print("Generated hex: ", hex_str)
print("Match with SU: ", hex_str == su_hex if len(su_hex) == len(hex_str) else "length mismatch")
