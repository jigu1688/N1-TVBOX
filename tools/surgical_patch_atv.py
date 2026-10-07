import shutil
import os

orig_dir = "tools/re_tools/orig_decomp/smali"
target_dir = "tools/re_tools/atv_decompiled/smali"

# 1. Restore clean original smali files
shutil.copy2(os.path.join(orig_dir, "ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"),
             os.path.join(target_dir, "ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"))

shutil.copy2(os.path.join(orig_dir, "ca/dstudio/atvlauncher/room/database/LauncherDatabase$a.smali"),
             os.path.join(target_dir, "ca/dstudio/atvlauncher/room/database/LauncherDatabase$a.smali"))

shutil.copy2(os.path.join(orig_dir, "y1/h.smali"), os.path.join(target_dir, "y1/h.smali"))
shutil.copy2(os.path.join(orig_dir, "y1/i$k.smali"), os.path.join(target_dir, "y1/i$k.smali"))
shutil.copy2(os.path.join(orig_dir, "z1/b.smali"), os.path.join(target_dir, "z1/b.smali"))

print("[1] Restored clean original Smali files from base APK.")

# 2. Patch LauncherDatabase_Impl$a.smali method a(Ld1/b;)V
impl_smali = os.path.join(target_dir, "ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali")
with open(impl_smali, 'r', encoding='utf-8') as f:
    lines = f.readlines()

patch_lines = [
    '\n',
    '    # --- Preset Sections & Settings ---\n',
    '    const-string v0, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'b37bda62-b1b6-4c0a-951c-e7b353919064\', \'WIDGET_SECTION\', 1, 0, 0, 0, \'小组件\', 0, 0, \'POSITION\', \'VERTICAL\', 0, 0, 3);"\n',
    '\n',
    '    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V\n',
    '\n',
    '    const-string v0, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'4355e037-d041-442f-b38a-3a31c0a91c7e\', \'APPLICATION_SECTION\', 0, 0, 1, 1, \'影音播放\', 1, 1, \'POSITION\', \'VERTICAL\', 150, 1, 5);"\n',
    '\n',
    '    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V\n',
    '\n',
    '    const-string v0, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'c28e1d23-4567-4890-abcd-ef0123456789\', \'APPLICATION_SECTION\', 0, 1, 1, 1, \'应用程序\', 1, 2, \'POSITION\', \'VERTICAL\', 150, 1, 5);"\n',
    '\n',
    '    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V\n',
    '\n',
    '    const-string v0, "INSERT OR REPLACE INTO `settings` (`key`, `value`) VALUES (\'settings-application-wallpaper-mode\', \'true\');"\n',
    '\n',
    '    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V\n'
]

new_lines = []
for i, line in enumerate(lines):
    if i < 90 and line.strip() == "return-void":
        new_lines.extend(patch_lines)
        new_lines.append(line)
    else:
        new_lines.append(line)

with open(impl_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)
print("[2] Successfully patched LauncherDatabase_Impl$a.smali method a!")

# 3. Patch z1/b.smali (Card radius -> 16px)
b_smali = os.path.join(target_dir, "z1/b.smali")
with open(b_smali, 'r', encoding='utf-8') as f:
    b_c = f.read()
b_c = b_c.replace("const/16 v0, 0x8", "const/16 v0, 0x10")
with open(b_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.write(b_c)
print("[3] Successfully patched z1/b.smali (16px border-radius)!")

# 4. Patch Application DAO Bindings in y1/i$k.smali
import patch_dao_bindings
print("[4] Successfully patched y1/i$k.smali DAO Bindings!")

print("[+] All Smali components patched cleanly and safely!")
