import os

k_smali = "tools/re_tools/atv_decompiled/smali/y1/i$k.smali"

with open(k_smali, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Intercept display-mode (index 15) -> always "VERTICAL"
old_display_mode = """    iget v0, p2, Lz1/b;->r:I

    invoke-static {v0}, Lx1/a;->f(I)Ljava/lang/String;

    move-result-object v0

    const/16 v1, 0xf

    if-nez v0, :cond_9

    invoke-interface {p1, v1}, Lc1/d;->l(I)V

    goto :goto_9

    :cond_9
    invoke-interface {p1, v0, v1}, Lc1/d;->y(Ljava/lang/String;I)V

    :goto_9"""

new_display_mode = """    const-string v0, "VERTICAL"

    const/16 v1, 0xf

    invoke-interface {p1, v0, v1}, Lc1/d;->y(Ljava/lang/String;I)V

    :goto_9"""

content = content.replace(old_display_mode, new_display_mode)

# 2. Intercept border-radius (index 16) -> always 16
old_radius = """    iget v0, p2, Lz1/b;->s:I

    int-to-long v0, v0

    const/16 v2, 0x10

    invoke-interface {p1, v2, v0, v1}, Lc1/d;->u(IJ)V"""

new_radius = """    const-wide/16 v0, 0x10

    const/16 v2, 0x10

    invoke-interface {p1, v2, v0, v1}, Lc1/d;->u(IJ)V"""

content = content.replace(old_radius, new_radius)

# 3. Intercept section-uuid (index 19) -> smart group routing
old_section = """    iget-object v0, p2, Lz1/h;->b:Ljava/lang/String;

    const/16 v1, 0x13

    if-nez v0, :cond_b

    invoke-interface {p1, v1}, Lc1/d;->l(I)V

    goto :goto_b

    :cond_b
    invoke-interface {p1, v0, v1}, Lc1/d;->y(Ljava/lang/String;I)V

    :goto_b"""

new_section = """    iget-object v0, p2, Lz1/a;->u:Ljava/lang/String;

    const-string v2, "com.hpplay.happyplay.aw"

    invoke-virtual {v2, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v2

    if-nez v2, :cond_dao_media

    const-string v2, "org.xbmc.kodi"

    invoke-virtual {v2, v0}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z

    move-result v0

    if-eqz v0, :cond_dao_apps

    :cond_dao_media
    const-string v0, "4355e037-d041-442f-b38a-3a31c0a91c7e"

    goto :cond_dao_apply

    :cond_dao_apps
    const-string v0, "c28e1d23-4567-4890-abcd-ef0123456789"

    :cond_dao_apply
    const/16 v1, 0x13

    invoke-interface {p1, v0, v1}, Lc1/d;->y(Ljava/lang/String;I)V

    :goto_b"""

content = content.replace(old_section, new_section)

# 4. Intercept background-type (index 24) -> always SOLID_COLOR
old_bg_type = """    iget v0, p2, Lz1/h;->g:I

    invoke-static {v0}, Lx1/a;->g(I)Ljava/lang/String;

    move-result-object v0

    const/16 v1, 0x18"""

new_bg_type = """    const-string v0, "SOLID_COLOR"

    const/16 v1, 0x18"""

content = content.replace(old_bg_type, new_bg_type)

with open(k_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print("[+] Successfully patched y1/i$k.smali DAO Bindings!")
