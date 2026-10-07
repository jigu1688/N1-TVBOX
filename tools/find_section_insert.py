import os, re

base_dir = "tools/re_tools/atv_decompiled/smali"

matches = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.smali'):
            fpath = os.path.join(root, f)
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                # Check for inserting sections
                if "INSERT INTO `sections`" in content or "INSERT INTO sections" in content or "APPLICATION_SECTION" in content:
                    rel = os.path.relpath(fpath, base_dir)
                    matches.append((rel, fpath))

print(f"Found {len(matches)} files referencing sections insert or APPLICATION_SECTION:")
for rel, fpath in matches:
    print(f"\n--- {rel} ---")
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
        lines = fp.readlines()
        for i, l in enumerate(lines):
            if any(k in l for k in ['INSERT INTO `sections`', 'APPLICATION_SECTION', 'WIDGET_SECTION', 'sections']):
                start = max(0, i - 2)
                end = min(len(lines), i + 10)
                print(f"Line {i+1}:")
                print("".join(lines[start:end]))
                print("." * 30)
