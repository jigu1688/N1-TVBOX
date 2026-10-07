import os, re

base_dir = "tools/re_tools/atv_decompiled/smali"

# Search for all places setting section-uuid on applications or calling insert application
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()
                for i, line in enumerate(lines):
                    if "iput-object" in line and "->b:Ljava/lang/String;" in line:
                        rel = os.path.relpath(p, base_dir)
                        print(f"[{rel}:{i+1}] {line.strip()}")
                        start = max(0, i-5)
                        end = min(len(lines), i+6)
                        print("".join(lines[start:end]))
                        print("="*50)
