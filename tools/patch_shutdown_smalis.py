import os

def patch_shutdown_smalis():
    # 1. ShutdownActivity$1 (Timer countdown finish -> svc power shutdown)
    path_1 = 'tools/re_tools/tvsettings_decompiled/smali/com/android/tv/settings/ShutdownActivity$1.smali'
    if os.path.exists(path_1):
        with open(path_1, 'r', encoding='utf-8') as f:
            c1 = f.read()
        target_1 = """    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v0

    const-string v1, "su -c killall com.droidlogic.BluetoothRemote"

    invoke-virtual {v0, v1}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;

    move-result-object v1

    invoke-virtual {v1}, Ljava/lang/Process;->waitFor()I

    const-string v1, "su -c reboot -p"

    invoke-virtual {v0, v1}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;

    move-result-object v1"""
        replacement_1 = """    :try_start_0
    invoke-static {}, Ljava/lang/Runtime;->getRuntime()Ljava/lang/Runtime;

    move-result-object v0

    const-string v1, "svc power shutdown"

    invoke-virtual {v0, v1}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0

    :catch_0"""
        if target_1 in c1:
            c1 = c1.replace(target_1, replacement_1)
            with open(path_1, 'w', encoding='utf-8') as f:
                f.write(c1)
            print("[+] Patched ShutdownActivity$1.smali successfully!")

    # 2. ShutdownActivity$2 (ArcView click -> svc power shutdown)
    path_2 = 'tools/re_tools/tvsettings_decompiled/smali/com/android/tv/settings/ShutdownActivity$2.smali'
    if os.path.exists(path_2):
        with open(path_2, 'r', encoding='utf-8') as f:
            c2 = f.read()
        if target_1 in c2:
            c2 = c2.replace(target_1, replacement_1)
            with open(path_2, 'w', encoding='utf-8') as f:
                f.write(c2)
            print("[+] Patched ShutdownActivity$2.smali successfully!")

    # 3. ShutdownActivity$5 (Shutdown button click -> svc power shutdown)
    path_5 = 'tools/re_tools/tvsettings_decompiled/smali/com/android/tv/settings/ShutdownActivity$5.smali'
    if os.path.exists(path_5):
        with open(path_5, 'r', encoding='utf-8') as f:
            c5 = f.read()
        if target_1 in c5:
            c5 = c5.replace(target_1, replacement_1)
            with open(path_5, 'w', encoding='utf-8') as f:
                f.write(c5)
            print("[+] Patched ShutdownActivity$5.smali successfully!")

    # 4. ShutdownActivity$4 (Sleep/U-disk Boot button -> mPowerManager.reboot("update"))
    path_4 = 'tools/re_tools/tvsettings_decompiled/smali/com/android/tv/settings/ShutdownActivity$4.smali'
    if os.path.exists(path_4):
        with open(path_4, 'r', encoding='utf-8') as f:
            c4 = f.read()
        target_4 = """    const-string v1, "su -c reboot update"

    invoke-virtual {v0, v1}, Ljava/lang/Runtime;->exec(Ljava/lang/String;)Ljava/lang/Process;"""
        replacement_4 = """    iget-object v0, p0, Lcom/android/tv/settings/ShutdownActivity$4;->this$0:Lcom/android/tv/settings/ShutdownActivity;

    iget-object v0, v0, Lcom/android/tv/settings/ShutdownActivity;->mPowerManager:Landroid/os/PowerManager;

    const-string/jumbo v1, "update"

    invoke-virtual {v0, v1}, Landroid/os/PowerManager;->reboot(Ljava/lang/String;)V"""
        if target_4 in c4:
            c4 = c4.replace(target_4, replacement_4)
            with open(path_4, 'w', encoding='utf-8') as f:
                f.write(c4)
            print("[+] Patched ShutdownActivity$4.smali successfully!")

if __name__ == '__main__':
    patch_shutdown_smalis()
