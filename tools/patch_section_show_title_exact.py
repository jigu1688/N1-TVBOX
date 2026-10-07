import os

# 1. Patch y1/i$u.smali
u_smali = "tools/re_tools/atv_decompiled/smali/y1/i$u.smali"
with open(u_smali, 'r', encoding='utf-8') as f:
    c = f.read()

target_u = """    iget-boolean v0, p2, Lz1/d;->h:Z

    const/16 v2, 0x8

    int-to-long v3, v0

    invoke-interface {p1, v2, v3, v4}, Lc1/d;->u(IJ)V"""

replace_u = """    const/16 v2, 0x8

    const-wide/16 v3, 0x1

    invoke-interface {p1, v2, v3, v4}, Lc1/d;->u(IJ)V"""

if target_u in c:
    c = c.replace(target_u, replace_u)
    with open(u_smali, 'w', encoding='utf-8', newline='\n') as f:
        f.write(c)
    print("[+] Successfully forced show-title=1 in y1/i$u.smali!")
else:
    print("Warning: target_u not found in y1/i$u.smali")

# 2. Patch y1/i$f.smali
f_smali = "tools/re_tools/atv_decompiled/smali/y1/i$f.smali"
if os.path.exists(f_smali):
    with open(f_smali, 'r', encoding='utf-8') as f:
        fc = f.read()
    if target_u in fc:
        fc = fc.replace(target_u, replace_u)
        with open(f_smali, 'w', encoding='utf-8', newline='\n') as f:
            f.write(fc)
        print("[+] Successfully forced show-title=1 in y1/i$f.smali!")
