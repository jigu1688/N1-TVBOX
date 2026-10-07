import os

files_to_inspect = [
    "smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase$a.smali",
    "smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali",
    "smali/a0/a.smali",
    "smali/x1/a.smali",
    "smali/a0/c.smali",
    "smali/y0/m$a.smali"
]

base_dir = "tools/re_tools/atv_decompiled"

for rel in files_to_inspect:
    p = os.path.join(base_dir, rel)
    print(f"\n{'='*60}\nFILE: {rel}\n{'='*60}")
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            print(f"Total lines: {len(lines)}")
            for i, line in enumerate(lines):
                if any(k in line for k in ['sections', 'APPLICATION', 'WIDGET', 'INSERT', 'default', 'create', 'populate', 'onCreate', 'onOpen']):
                    start = max(0, i-3)
                    end = min(len(lines), i+15)
                    print(f"--- Line {i+1} ---")
                    print("".join(lines[start:end]))
                    print("-" * 40)
                    break
