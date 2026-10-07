import shutil
import os

orig_dir = "tools/re_tools/orig_decomp/smali"
target_dir = "tools/re_tools/atv_decompiled/smali"

# 1. Fully restore ALL smali files from pure orig_decomp
for root, dirs, files in os.walk(orig_dir):
    rel_path = os.path.relpath(root, orig_dir)
    target_subdir = os.path.join(target_dir, rel_path)
    os.makedirs(target_subdir, exist_ok=True)
    for f in files:
        shutil.copy2(os.path.join(root, f), os.path.join(target_subdir, f))

print("[1] Fully restored ALL Smali files to 100% pure base APK.")

# 2. Patch z1/b.smali (16px border-radius)
b_smali = os.path.join(target_dir, "z1/b.smali")
with open(b_smali, 'r', encoding='utf-8') as f:
    b_c = f.read()
b_c = b_c.replace("const/16 v0, 0x8", "const/16 v0, 0x10")
with open(b_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.write(b_c)
print("[2] Patched z1/b.smali (16px border-radius)")

# 3. Patch y1/i$k.smali (DAO bindings for solid colors, vertical cards, 16px radius and section groups)
import patch_dao_bindings
print("[3] Patched y1/i$k.smali DAO Bindings")

# 4. Patch y1/h.smali (Dual section creation in method c and method w)
import patch_atv_engine
import patch_smart_routing
print("[4] Patched y1/h.smali Dual Section Engine & Smart Routing")

# 5. Patch Section DAO (Force show-title=1)
import patch_section_show_title_exact
print("[5] Patched Section DAO (Force show-title=1)")

print("[+] All clean patches applied successfully!")
