import os

base = "tools/re_tools/atv_decompiled/smali/y1"
for f in os.listdir(base):
    if f.startswith("i$"):
        p = os.path.join(base, f)
        with open(p, 'r', encoding='utf-8') as fp:
            c = fp.read()
            if "INSERT OR REPLACE INTO `sections`" in c or "INSERT OR ABORT INTO `sections`" in c or "INSERT INTO `sections`" in c:
                print(f"=== Found Section DAO in {f} ===")
                print(c[:1500])
