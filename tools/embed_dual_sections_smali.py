import os

smali_path = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"

with open(smali_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = """    const-string v0, "INSERT OR REPLACE INTO room_master_table (id,identity_hash) VALUES(42, \\'344604a56ef748d25999b6487b7cbc3c\\')"

    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V

    return-void"""

replacement = """    const-string v0, "INSERT OR REPLACE INTO room_master_table (id,identity_hash) VALUES(42, \\'344604a56ef748d25999b6487b7cbc3c\\')"

    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V

    # --- Native Dual Section & Settings Preset ---
    const-string v0, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'b37bda62-b1b6-4c0a-951c-e7b353919064\', \'WIDGET_SECTION\', 1, 0, 0, 0, \'小组件\', 0, 0, \'POSITION\', \'VERTICAL\', 0, 0, 3);"
    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V

    const-string v0, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'4355e037-d041-442f-b38a-3a31c0a91c7e\', \'APPLICATION_SECTION\', 0, 0, 1, 1, \'影音播放\', 1, 1, \'POSITION\', \'VERTICAL\', 150, 1, 5);"
    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V

    const-string v0, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'c28e1d23-4567-4890-abcd-ef0123456789\', \'APPLICATION_SECTION\', 0, 1, 1, 1, \'应用程序\', 1, 2, \'POSITION\', \'VERTICAL\', 150, 1, 5);"
    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V

    const-string v0, "INSERT OR REPLACE INTO `settings` (`key`, `value`) VALUES (\'settings-application-wallpaper-mode\', \'true\');"
    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V

    return-void"""

if target in content:
    new_content = content.replace(target, replacement)
    with open(smali_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    print("[+] Successfully embedded Dual Sections & Wallpaper Settings directly into Room SQLite onCreate Smali!")
else:
    raise ValueError("Target pattern not found in LauncherDatabase_Impl$a.smali")
