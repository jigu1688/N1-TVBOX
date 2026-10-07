import os

smali_path = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase$a.smali"

with open(smali_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = "sput-object v1, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;->m:Lca/dstudio/atvlauncher/room/database/LauncherDatabase;"

injected = """sput-object v1, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;->m:Lca/dstudio/atvlauncher/room/database/LauncherDatabase;

    # --- Custom Native Master Layout Inserter ---
    :try_start_custom
    invoke-virtual {v1}, Ly0/m;->h()Lc1/c;
    move-result-object v2
    invoke-interface {v2}, Lc1/c;->B()Lc1/b;
    move-result-object v2

    const-string v3, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'b37bda62-b1b6-4c0a-951c-e7b353919064\', \'WIDGET_SECTION\', 1, 0, 0, 0, \'小组件\', 0, 0, \'POSITION\', \'VERTICAL\', 0, 0, 3);"
    invoke-interface {v2, v3}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v3, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'4355e037-d041-442f-b38a-3a31c0a91c7e\', \'APPLICATION_SECTION\', 0, 0, 1, 1, \'影音播放\', 1, 1, \'POSITION\', \'VERTICAL\', 150, 1, 5);"
    invoke-interface {v2, v3}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v3, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'c28e1d23-4567-4890-abcd-ef0123456789\', \'APPLICATION_SECTION\', 0, 1, 1, 1, \'应用程序\', 1, 2, \'POSITION\', \'VERTICAL\', 150, 1, 5);"
    invoke-interface {v2, v3}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v3, "INSERT OR REPLACE INTO `settings` (`key`, `value`) VALUES (\'settings-application-wallpaper-mode\', \'true\');"
    invoke-interface {v2, v3}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v3, "UPDATE `applications` SET `section-uuid`=\'4355e037-d041-442f-b38a-3a31c0a91c7e\', `position`=0 WHERE `package-name`=\'com.hpplay.happyplay.aw\';"
    invoke-interface {v2, v3}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v3, "UPDATE `applications` SET `border-radius`=16, `display-mode`=\'VERTICAL\';"
    invoke-interface {v2, v3}, Lc1/b;->g(Ljava/lang/String;)V
    :try_end_custom
    .catchall {:try_start_custom .. :try_end_custom} :catchall_custom

    goto :goto_custom_ok

    :catchall_custom
    move-exception v2
    :goto_custom_ok
"""

if target in content:
    new_content = content.replace(target, injected)
    with open(smali_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)
    print("[+] Successfully injected Master Inserter into LauncherDatabase$a.smali!")
else:
    raise ValueError("Target not found in LauncherDatabase$a.smali")
