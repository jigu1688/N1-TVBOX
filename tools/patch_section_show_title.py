import os

# 1. Patch y1/i$u.smali (Section INSERT DAO binder)
u_smali = "tools/re_tools/atv_decompiled/smali/y1/i$u.smali"
with open(u_smali, 'r', encoding='utf-8') as f:
    u_lines = f.readlines()

for i, line in enumerate(u_lines):
    # Param 8 is show-title
    if "const/16 v2, 0x8" in line:
        # replace previous line 'int-to-long v3, v0' with 'const-wide/16 v3, 0x1'
        if i > 0 and "int-to-long v3, v0" in u_lines[i-1]:
            u_lines[i-1] = "    const-wide/16 v3, 0x1\n"
            print("[+] Force-enabled show-title=1 in y1/i$u.smali (Section Insert DAO)")

with open(u_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(u_lines)

# 2. Patch y1/i$f.smali (Section UPDATE DAO binder)
f_smali = "tools/re_tools/atv_decompiled/smali/y1/i$f.smali"
if os.path.exists(f_smali):
    with open(f_smali, 'r', encoding='utf-8') as f:
        f_lines = f.readlines()

    for i, line in enumerate(f_lines):
        if "const/16 v2, 0x8" in line or "const/16 v1, 0x8" in line or "const/16 v0, 0x8" in line:
            # force true
            for offset in [-1, -2]:
                if "int-to-long" in f_lines[i+offset]:
                    reg = f_lines[i+offset].strip().split()[1].replace(',', '')
                    f_lines[i+offset] = f"    const-wide/16 {reg}, 0x1\n"
                    print(f"[+] Force-enabled show-title=1 in y1/i$f.smali (Section Update DAO)")

    with open(f_smali, 'w', encoding='utf-8', newline='\n') as f:
        f_lines_text = "".join(f_lines)
        with open(f_smali, 'w', encoding='utf-8', newline='\n') as fp:
            fp.write(f_lines_text)

print("[+] Section Title Enforcement Patches applied!")
