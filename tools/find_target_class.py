import capstone

with open('tools/re_tools/libsystemcontrolservice.so', 'rb') as f:
    elf = f.read()

md = capstone.Cs(capstone.CS_ARCH_ARM, capstone.CS_MODE_THUMB)

# Look at code around each method to see Parcel writing (e.g., writeString, writeInt32)
for code_id, addr in [(1, 0x60e8), (2, 0x61c0), (3, 0x62a4), (4, 0x6354)]:
    print(f"\n=== Transaction Code {code_id} (around 0x{addr:x}) ===")
    code = elf[addr:addr+100]
    for insn in md.disasm(code, addr):
        print(f"  0x{insn.address:x}: {insn.mnemonic}\t{insn.op_str}")
        if insn.mnemonic == 'blx' and 'r7' in insn.op_str:
            break
