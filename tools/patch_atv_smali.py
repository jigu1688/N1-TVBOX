import os

smali_path = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"

with open(smali_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

sqls = [
    # 1. Widget section (hidden)
    "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES ('b37bda62-b1b6-4c0a-951c-e7b353919064', 'WIDGET_SECTION', 1, 0, 0, 0, '小组件', 0, 0, 'POSITION', 'VERTICAL', 0, 0, 3);",
    
    # 2. Section 1: 影音播放 (Row 1, 5 cols, 150px)
    "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES ('4355e037-d041-442f-b38a-3a31c0a91c7e', 'APPLICATION_SECTION', 0, 0, 1, 1, '影音播放', 1, 1, 'POSITION', 'VERTICAL', 150, 1, 5);",
    
    # 3. Section 2: 应用程序 (Row 2, 5 cols, 150px, primary=1 for newly scanned apps)
    "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES ('c28e1d23-4567-4890-abcd-ef0123456789', 'APPLICATION_SECTION', 0, 1, 1, 1, '应用程序', 1, 2, 'POSITION', 'VERTICAL', 150, 1, 5);",
    
    # 4. Settings: enable wallpaper mode
    "INSERT OR REPLACE INTO `settings` (`key`, `value`) VALUES ('settings-application-wallpaper-mode', 'true');",
    
    # 5. 乐播投屏 -> 影音播放
    "INSERT OR REPLACE INTO `applications` (`package-name`, `class-name`, `version-name`, `version-code`, `sticky`, `show-title`, `icon-scale`, `show-icon`, `show-shadow`, `display-mode`, `border-radius`, `launch-count`, `uuid`, `section-uuid`, `resource-version`, `position`, `visibility`, `state`, `background-type`, `background-color`) VALUES ('com.hpplay.happyplay.aw', 'com.hpplay.happyplay.aw.SplashActivity', 'v1', 1, 0, 1, 1, 1, 1, 'VERTICAL', 16, 0, 'app-uuid-hpplay', '4355e037-d041-442f-b38a-3a31c0a91c7e', 'v1', 0, 'VISIBLE', 'ACTIVE', 'SOLID_COLOR', -14314529);",
    
    # 6. 隔空传装 -> 应用程序
    "INSERT OR REPLACE INTO `applications` (`package-name`, `class-name`, `version-name`, `version-code`, `sticky`, `show-title`, `icon-scale`, `show-icon`, `show-shadow`, `display-mode`, `border-radius`, `launch-count`, `uuid`, `section-uuid`, `resource-version`, `position`, `visibility`, `state`, `background-type`, `background-color`) VALUES ('com.nextgen.webpush', 'com.nextgen.webpush.MainActivity', 'v1', 1, 0, 1, 1, 1, 1, 'VERTICAL', 16, 0, 'app-uuid-webpush', 'c28e1d23-4567-4890-abcd-ef0123456789', 'v1', 0, 'VISIBLE', 'ACTIVE', 'SOLID_COLOR', -8963627);",
    
    # 7. 文件管理器 -> 应用程序
    "INSERT OR REPLACE INTO `applications` (`package-name`, `class-name`, `version-name`, `version-code`, `sticky`, `show-title`, `icon-scale`, `show-icon`, `show-shadow`, `display-mode`, `border-radius`, `launch-count`, `uuid`, `section-uuid`, `resource-version`, `position`, `visibility`, `state`, `background-type`, `background-color`) VALUES ('com.droidlogic.FileBrower', 'com.droidlogic.FileBrower.FileBrower', 'v1', 1, 0, 1, 1, 1, 1, 'VERTICAL', 16, 0, 'app-uuid-fb', 'c28e1d23-4567-4890-abcd-ef0123456789', 'v1', 1, 'VISIBLE', 'ACTIVE', 'SOLID_COLOR', -14705564);",
    
    # 8. 设置 -> 应用程序
    "INSERT OR REPLACE INTO `applications` (`package-name`, `class-name`, `version-name`, `version-code`, `sticky`, `show-title`, `icon-scale`, `show-icon`, `show-shadow`, `display-mode`, `border-radius`, `launch-count`, `uuid`, `section-uuid`, `resource-version`, `position`, `visibility`, `state`, `background-type`, `background-color`) VALUES ('com.android.settings', 'com.android.settings.Settings', 'v1', 1, 0, 1, 1, 1, 1, 'VERTICAL', 16, 0, 'app-uuid-settings', 'c28e1d23-4567-4890-abcd-ef0123456789', 'v1', 2, 'VISIBLE', 'ACTIVE', 'SOLID_COLOR', -7697782);",
    
    # 9. ATV桌面 -> 应用程序
    "INSERT OR REPLACE INTO `applications` (`package-name`, `class-name`, `version-name`, `version-code`, `sticky`, `show-title`, `icon-scale`, `show-icon`, `show-shadow`, `display-mode`, `border-radius`, `launch-count`, `uuid`, `section-uuid`, `resource-version`, `position`, `visibility`, `state`, `background-type`, `background-color`) VALUES ('ca.dstudio.atvlauncher.pro', 'ca.dstudio.atvlauncher.screens.launcher.LauncherActivity', 'v1', 1, 0, 1, 1, 1, 1, 'VERTICAL', 16, 0, 'app-uuid-atv', 'c28e1d23-4567-4890-abcd-ef0123456789', 'v1', 3, 'VISIBLE', 'ACTIVE', 'SOLID_COLOR', -13654050);"
]

injected_smali_lines = []
for sql in sqls:
    escaped = sql.replace("'", "\\'")
    injected_smali_lines.append(f'    const-string v0, "{escaped}"\n\n')
    injected_smali_lines.append('    invoke-virtual {p1, v0}, Ld1/b;->g(Ljava/lang/String;)V\n\n')

new_lines = []
found_target = False

for i, line in enumerate(lines):
    if not found_target and line.strip() == "return-void" and i < 100:
        # We are at the end of method a(Ld1/b;)V
        new_lines.extend(injected_smali_lines)
        new_lines.append(line)
        found_target = True
    else:
        new_lines.append(line)

if not found_target:
    raise ValueError("Could not find return-void in method a(Ld1/b;)V!")

with open(smali_path, 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print(f"[+] Successfully patched {smali_path} with {len(sqls)} hardcoded master layout SQLs!")
