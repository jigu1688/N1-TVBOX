import os, re

base_dir = "tools/re_tools/atv_decompiled"
public_xml = os.path.join(base_dir, "res/values/public.xml")

with open(public_xml, 'r', encoding='utf-8') as f:
    for line in f:
        if 'name="application_section_title"' in line:
            print("application_section_title ID:", line.strip())
            # extract id hex
            m = re.search(r'id="([^"]+)"', line)
            if m:
                hex_id = m.group(1)
                print("Hex ID:", hex_id)

                # Search all smali files for this hex id
                for root, dirs, files in os.walk(os.path.join(base_dir, "smali")):
                    for f2 in files:
                        if f2.endswith('.smali'):
                            p = os.path.join(root, f2)
                            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                                c = fp.read()
                                if hex_id in c or "application_section_title" in c:
                                    print("Found in smali:", os.path.relpath(p, base_dir))
