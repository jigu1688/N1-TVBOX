import os, re

base_dir = "tools/re_tools/atv_decompiled"

# 1. Search in strings.xml for "应用程序" or "Applications"
strings_xml = os.path.join(base_dir, "res/values-zh-rCN/strings.xml")
res_name = None
if os.path.exists(strings_xml):
    with open(strings_xml, 'r', encoding='utf-8') as f:
        for line in f:
            if "应用程序" in line:
                print("Found in strings-zh:", line.strip())
                # extract string name
                m = re.search(r'name="([^"]+)"', line)
                if m:
                    res_name = m.group(1)
                    print("  Res name:", res_name)

# 2. Search for public ID of this string
if res_name:
    public_xml = os.path.join(base_dir, "res/values/public.xml")
    if os.path.exists(public_xml):
        with open(public_xml, 'r', encoding='utf-8') as f:
            for line in f:
                if f'name="{res_name}"' in line:
                    print("Public ID:", line.strip())

# 3. Search all smali files for references to this string or default section creation
for root, dirs, files in os.walk(os.path.join(base_dir, "smali")):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if res_name and res_name in c:
                    print(f"Smali referencing {res_name}:", os.path.relpath(p, base_dir))
                if "APPLICATION_SECTION" in c:
                    print("Smali with APPLICATION_SECTION:", os.path.relpath(p, base_dir))
