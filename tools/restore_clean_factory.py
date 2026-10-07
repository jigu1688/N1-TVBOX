clean_factory_smali = """.class public final Lca/dstudio/atvlauncher/room/database/LauncherDatabase$a;
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

    return-object p0
.end method
"""

smali_path = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase$a.smali"
with open(smali_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(clean_factory_smali)

print("[+] Reverted LauncherDatabase$a.smali to clean, thread-safe Room builder!")
