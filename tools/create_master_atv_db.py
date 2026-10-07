import sqlite3
import shutil
import os
import uuid

def create_master_db():
    print("[*] Generating Official Pure ATV Launcher Master Database (International Clean Baseline)...")
    src_db = 'logs/sections.db'
    dst_db = 'build_rom/system_root/etc/atvlauncher/sections.db'
    os.makedirs(os.path.dirname(dst_db), exist_ok=True)
    shutil.copy2(src_db, dst_db)

    conn = sqlite3.connect(dst_db)
    c = conn.cursor()

    # Disable WAL mode and enforce standard single-file DELETE mode
    c.execute("PRAGMA journal_mode = DELETE;")

    sec_widget_uuid = '39971e9a-e104-4b15-967a-83f55cac2e6e'
    sec_apps_uuid   = 'c28e1d23-4567-4890-abcd-ef0123456789'

    # Clear all sections
    c.execute("DELETE FROM sections")

    # 1. Widgets Section (Position 0, 1 row 3 cols, height 490)
    c.execute("""
        INSERT INTO sections (
            [uuid], [type], [sticky], [primary], [always-visible], [visible], 
            [title], [show-title], [position], [sorting-order], [orientation], 
            [item-height], [rows], [cols]
        ) VALUES (
            ?, 'WIDGET_SECTION', 1, 1, 1, 1, 
            '小组件', 0, 0, 'POSITION', 'VERTICAL', 
            490, 1, 3
        )
    """, (sec_widget_uuid,))

    # Clean widgets table
    c.execute("DELETE FROM widgets")

    # 2. Main Applications Section (Position 1, 1 row 5 cols, height 150)
    c.execute("""
        INSERT INTO sections (
            [uuid], [type], [sticky], [primary], [always-visible], [visible], 
            [title], [show-title], [position], [sorting-order], [orientation], 
            [item-height], [rows], [cols]
        ) VALUES (
            ?, 'APPLICATION_SECTION', 1, 1, 1, 1, 
            '应用程序', 1, 1, 'POSITION', 'VERTICAL', 
            150, 1, 5
        )
    """, (sec_apps_uuid,))

    # Clean applications table and register pristine core apps
    c.execute("DELETE FROM applications")

    apps = [
        # (package, class, title, position, bg_color)
        ('com.google.android.gms', 'org.microg.gms.ui.SettingsActivity', 'microG 设置', 0, -16730734),
        ('com.nextgen.webpush', 'com.nextgen.webpush.MainActivity', '隔空传装', 1, -4342339),
        ('com.droidlogic.FileBrower', 'com.droidlogic.FileBrower.FileBrower', '文件管理', 2, -1263616),
        ('com.android.settings', 'com.android.settings.Settings', '设置', 3, -16730734),
        ('com.hpplay.happyplay.aw', 'com.hpplay.happyplay.aw.WelcomeActivity', '乐播投屏', 4, -16730734),
        ('ca.dstudio.atvlauncher.pro', 'ca.dstudio.atvlauncher.screens.launcher.LauncherActivity', 'ATV桌面', 5, -16730734),
    ]

    for pkg, cls, title, pos, bg in apps:
        app_uuid = str(uuid.uuid4())
        c.execute("""
            INSERT INTO applications (
                [package-name], [class-name], [version-name], [version-code],
                [activity-title], [activity-icon], [activity-banner], [sticky],
                [title], [show-title], [icon], [icon-scale], [show-icon], [show-shadow],
                [display-mode], [border-radius], [launch-count], [uuid], [section-uuid],
                [resource-version], [position], [visibility], [state], [background-type],
                [background-color], [background-image]
            ) VALUES (
                ?, ?, '1.0', 1,
                ?, NULL, NULL, 0,
                ?, 1, NULL, 100, 1, 1,
                'VERTICAL', 16, 0, ?, ?,
                'Sun Sep 01 2026', ?, 'VISIBLE', 'ACTIVE', 'SOLID_COLOR',
                ?, NULL
            )
        """, (pkg, cls, title, title, app_uuid, sec_apps_uuid, pos, bg))

    conn.commit()
    conn.close()
    print(f"[+] Master database generated with {len(apps)} pristine baseline apps!")

if __name__ == '__main__':
    create_master_db()
