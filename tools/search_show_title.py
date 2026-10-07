import os

base = "tools/re_tools/atv_decompiled/smali"
for root, dirs, files in os.walk(base):
    for f in files:
        if f.endswith(".smali"):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                for i, line in enumerate(fp):
                    if "->h:Z" in line or "show-title" in line:
                        print(f"[{os.path.relpath(p, base)}:{i+1}] {line.strip()}")
