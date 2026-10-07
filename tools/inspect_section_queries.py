import os

base = "tools/re_tools/atv_decompiled/smali/y1"
for f in ["h.smali", "i.smali"]:
    p = os.path.join(base, f)
    with open(p, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines):
            if "SELECT * FROM `sections`" in line or "SELECT * FROM sections" in line:
                print(f"[{f}:{i+1}] {line.strip()}")
                start = max(0, i-10)
                end = min(len(lines), i+30)
                print("".join(lines[start:end]))
                print("="*60)
