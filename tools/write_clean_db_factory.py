clean_smali = """.class public final Lca/dstudio/atvlauncher/room/database/LauncherDatabase$a;
.super Ljava/lang/Object;


# annotations
.annotation system Ldalvik/annotation/EnclosingClass;
    value = Lca/dstudio/atvlauncher/room/database/LauncherDatabase;
.end annotation

.annotation system Ldalvik/annotation/InnerClass;
    accessFlags = 0x19
    name = "a"
.end annotation


# direct methods
.method public static a(Landroid/content/Context;)Lca/dstudio/atvlauncher/room/database/LauncherDatabase;
    .locals 5

    const-string v0, "context"

    invoke-static {p0, v0}, Lo7/j;->e(Ljava/lang/Object;Ljava/lang/String;)V

    sget-object v0, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;->m:Lca/dstudio/atvlauncher/room/database/LauncherDatabase;

    if-nez v0, :cond_1

    const-class v0, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;

    invoke-static {v0}, Lo7/o;->a(Ljava/lang/Class;)Lo7/d;

    move-result-object v0

    monitor-enter v0

    :try_start_0
    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    move-result-object v1

    const-string v2, "context.applicationContext"

    invoke-static {v1, v2}, Lo7/j;->d(Ljava/lang/Object;Ljava/lang/String;)V

    const-string v2, "sections.db"

    invoke-static {v2}, Lv7/f;->M0(Ljava/lang/String;)Z

    move-result v2

    const/4 v3, 0x1

    xor-int/2addr v2, v3

    if-eqz v2, :cond_0

    new-instance v2, Ly0/m$a;

    invoke-direct {v2, v1}, Ly0/m$a;-><init>(Landroid/content/Context;)V

    new-array v1, v3, [Lz0/a;

    sget-object v3, La2/a;->a:La2/a$a;

    const/4 v4, 0x0

    aput-object v3, v1, v4

    invoke-virtual {v2, v1}, Ly0/m$a;->a([Lz0/a;)V

    invoke-virtual {v2}, Ly0/m$a;->b()Ly0/m;

    move-result-object v1

    check-cast v1, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;

    sput-object v1, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;->m:Lca/dstudio/atvlauncher/room/database/LauncherDatabase;

    invoke-virtual {p0}, Landroid/content/Context;->getApplicationContext()Landroid/content/Context;

    move-result-object p0

    const-string v2, "context.applicationContext"

    invoke-static {p0, v2}, Lo7/j;->d(Ljava/lang/Object;Ljava/lang/String;)V

    iput-object p0, v1, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;->l:Landroid/content/Context;
    :try_end_0
    .catchall {:try_start_0 .. :try_end_0} :catchall_0

    monitor-exit v0

    goto :goto_0

    :cond_0
    :try_start_1
    new-instance p0, Ljava/lang/IllegalArgumentException;

    const-string v1, "Cannot build a database with null or empty name. If you are trying to create an in memory database, use Room.inMemoryDatabaseBuilder"

    invoke-virtual {v1}, Ljava/lang/Object;->toString()Ljava/lang/String;

    move-result-object v1

    invoke-direct {p0, v1}, Ljava/lang/IllegalArgumentException;-><init>(Ljava/lang/String;)V

    throw p0
    :try_end_1
    .catchall {:try_start_1 .. :try_end_1} :catchall_0

    :catchall_0
    move-exception p0

    monitor-exit v0

    throw p0

    :cond_1
    :goto_0
    sget-object p0, Lca/dstudio/atvlauncher/room/database/LauncherDatabase;->m:Lca/dstudio/atvlauncher/room/database/LauncherDatabase;

    if-eqz p0, :cond_skip_init

    :try_start_init
    invoke-virtual {p0}, Ly0/m;->h()Lc1/c;
    move-result-object v0

    invoke-interface {v0}, Lc1/c;->B()Lc1/b;
    move-result-object v0

    const-string v1, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'b37bda62-b1b6-4c0a-951c-e7b353919064\', \'WIDGET_SECTION\', 1, 0, 0, 0, \'小组件\', 0, 0, \'POSITION\', \'VERTICAL\', 0, 0, 3);"
    invoke-interface {v0, v1}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v1, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'4355e037-d041-442f-b38a-3a31c0a91c7e\', \'APPLICATION_SECTION\', 0, 0, 1, 1, \'影音播放\', 1, 1, \'POSITION\', \'VERTICAL\', 150, 1, 5);"
    invoke-interface {v0, v1}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v1, "INSERT OR REPLACE INTO `sections` (`uuid`, `type`, `sticky`, `primary`, `always-visible`, `visible`, `title`, `show-title`, `position`, `sorting-order`, `orientation`, `item-height`, `rows`, `cols`) VALUES (\'c28e1d23-4567-4890-abcd-ef0123456789\', \'APPLICATION_SECTION\', 0, 1, 1, 1, \'应用程序\', 1, 2, \'POSITION\', \'VERTICAL\', 150, 1, 5);"
    invoke-interface {v0, v1}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v1, "INSERT OR REPLACE INTO `settings` (`key`, `value`) VALUES (\'settings-application-wallpaper-mode\', \'true\');"
    invoke-interface {v0, v1}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v1, "UPDATE `applications` SET `section-uuid`=\'4355e037-d041-442f-b38a-3a31c0a91c7e\', `position`=0 WHERE `package-name`=\'com.hpplay.happyplay.aw\';"
    invoke-interface {v0, v1}, Lc1/b;->g(Ljava/lang/String;)V

    const-string v1, "UPDATE `applications` SET `border-radius`=16, `display-mode`=\'VERTICAL\';"
    invoke-interface {v0, v1}, Lc1/b;->g(Ljava/lang/String;)V
    :try_end_init
    .catchall {:try_start_init .. :try_end_init} :catchall_init

    goto :cond_skip_init

    :catchall_init
    move-exception v0

    :cond_skip_init
    return-object p0
.end method
"""

smali_path = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase$a.smali"
with open(smali_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(clean_smali)

print("[+] Clean LauncherDatabase$a.smali written successfully!")
