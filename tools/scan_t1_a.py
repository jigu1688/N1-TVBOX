p = "tools/re_tools/atv_decompiled/smali/t1/a.smali"

with open(p, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['new-instance', 'Lz1/a;', 'section', 'sections', 'SOLID_COLOR', 'border-radius', 'VERTICAL']):
        start = max(0, i-2)
        end = min(len(lines), i+15)
        print(f"Line {i+1}:")
        print("".join(lines[start:end]))
        print("="*40)
