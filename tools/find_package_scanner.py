import os, re

base_dir = "tools/re_tools/atv_decompiled/smali"

# Search for classes that insert into applications table
app_dao_files = []

for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if 'INSERT INTO `applications`' in c or 'INSERT OR REPLACE INTO `applications`' in c:
                    app_dao_files.append(os.path.relpath(p, base_dir))

print("Files inserting into applications table:")
for f in app_dao_files:
    print("  -", f)

# Also check where applications are populated initially
pop_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith('.smali'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
                if 'getInstalledPackages' in c or 'getInstalledApplications' in c or 'queryIntentActivities' in c:
                    pop_files.append(os.path.relpath(p, base_dir))

print("\nFiles querying package manager for installed apps:")
for f in pop_files:
    print("  -", f)
