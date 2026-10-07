import os

p = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"

with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines in LauncherDatabase_Impl$a: {len(lines)}")

methods = []
current_method = []
in_method = False

for line in lines:
    if line.startswith('.method '):
        in_method = True
        current_method = [line]
    elif in_method:
        current_method.append(line)
        if line.startswith('.end method'):
            methods.append(current_method)
            in_method = False

for m in methods:
    m_head = m[0].strip()
    print(f"\n{'='*50}\nMethod: {m_head}\n{'='*50}")
    # print up to 50 lines
    for l in m[:50]:
        print(l, end='')
    if len(m) > 50:
        print(f"\n... ({len(m) - 50} more lines) ...\n")
