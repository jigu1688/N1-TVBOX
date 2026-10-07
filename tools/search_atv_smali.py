import os, re

base_dir = "tools/re_tools/atv_decompiled"

keywords = [
    "sections.db",
    "APPLICATION_SECTION",
    "WIDGET_SECTION",
    "room_master_table",
    "CREATE TABLE",
    "border-radius",
    "section-uuid",
    "restore",
    "backup",
    "onCreate",
    "RoomDatabase"
]

results = {k: [] for k in keywords}

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.smali') or f.endswith('.xml'):
            fpath = os.path.join(root, f)
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                    content = fp.read()
                    for k in keywords:
                        if k in content:
                            rel = os.path.relpath(fpath, base_dir)
                            results[k].append(rel)
            except Exception as e:
                pass

print("=== Search Results in ATV Launcher Smali ===")
for k, flist in results.items():
    print(f"\n[{k}] ({len(flist)} matches):")
    for f in flist[:8]:
        print("  -", f)
