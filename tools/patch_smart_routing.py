import os

h_smali = "tools/re_tools/atv_decompiled/smali/y1/h.smali"

with open(h_smali, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the unconditional section assignment with smart auto-grouping
target_block = """    invoke-static {v10, v9}, Lt1/a;->c(Landroid/content/Context;Landroid/content/ComponentName;)Lz1/a;

    move-result-object v9

    iget-object v10, v3, Lz1/d;->a:Ljava/lang/String;

    iput-object v10, v9, Lz1/h;->b:Ljava/lang/String;"""

replacement_block = """    invoke-static {v10, v9}, Lt1/a;->c(Landroid/content/Context;Landroid/content/ComponentName;)Lz1/a;

    move-result-object v9

    iget-object v10, v3, Lz1/d;->a:Ljava/lang/String;

    iput-object v10, v9, Lz1/h;->b:Ljava/lang/String;

    # Smart Routing: If hpplay or kodi, move to Media Section
    iget-object v10, v9, Lz1/a;->u:Ljava/lang/String;
    if-eqz v10, :cond_skip_route_first_scan
    const-string v11, "com.hpplay.happyplay.aw"
    invoke-virtual {v10, v11}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v11
    if-nez v11, :cond_to_media_first_scan
    const-string v11, "org.xbmc.kodi"
    invoke-virtual {v10, v11}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v10
    if-eqz v10, :cond_skip_route_first_scan

    :cond_to_media_first_scan
    const-string v10, "4355e037-d041-442f-b38a-3a31c0a91c7e"
    iput-object v10, v9, Lz1/h;->b:Ljava/lang/String;
    :cond_skip_route_first_scan"""

content_new = content.replace(target_block, replacement_block)

# Also check around line 2491
target_block2 = """    iget-object v10, v4, Lz1/d;->a:Ljava/lang/String;

    iput-object v10, v9, Lz1/h;->b:Ljava/lang/String;"""

replacement_block2 = """    iget-object v10, v4, Lz1/d;->a:Ljava/lang/String;

    iput-object v10, v9, Lz1/h;->b:Ljava/lang/String;

    iget-object v10, v9, Lz1/a;->u:Ljava/lang/String;
    if-eqz v10, :cond_skip_route_second_scan
    const-string v11, "com.hpplay.happyplay.aw"
    invoke-virtual {v10, v11}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v11
    if-nez v11, :cond_to_media_second_scan
    const-string v11, "org.xbmc.kodi"
    invoke-virtual {v10, v11}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v10
    if-eqz v10, :cond_skip_route_second_scan

    :cond_to_media_second_scan
    const-string v10, "4355e037-d041-442f-b38a-3a31c0a91c7e"
    iput-object v10, v9, Lz1/h;->b:Ljava/lang/String;
    :cond_skip_route_second_scan"""

content_new = content_new.replace(target_block2, replacement_block2)

with open(h_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content_new)

print("[+] Successfully patched y1/h.smali smart media routing with unique labels!")
