p = "tools/re_tools/atv_decompiled/smali/t1/a.smali"

with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if "new-instance" in l and "Lz1/a;" in l:
        start = max(0, i-5)
        end = min(len(lines), i+60)
        print(f"Line {i+1}:")
        print("".join(lines[start:end]))
        print("="*60)
