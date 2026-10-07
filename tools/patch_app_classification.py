import os

t1_smali = "tools/re_tools/atv_decompiled/smali/t1/a.smali"
with open(t1_smali, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Target insertion point in method c: right before "return-object v0" around line 339
patch_smali = """
    # --- Custom Native Auto-Classification & Styling Patch ---
    const/4 v1, 0x1
    iput v1, v0, Lz1/b;->r:I # display-mode = VERTICAL (1)
    const/16 v1, 0x10
    iput v1, v0, Lz1/b;->s:I # border-radius = 16

    iget-object v1, v0, Lz1/a;->u:Ljava/lang/String;

    # Check if 乐播投屏 or Kodi
    const-string v2, "com.hpplay.happyplay.aw"
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :cond_custom_kodi

    const-string v2, "4355e037-d041-442f-b38a-3a31c0a91c7e"
    iput-object v2, v0, Lz1/h;->b:Ljava/lang/String;
    const v2, -14314529
    iput v2, v0, Lz1/h;->g:I
    const/4 v2, 0x0
    iput v2, v0, Lz1/h;->d:I
    goto :goto_custom_end

    :cond_custom_kodi
    const-string v2, "org.xbmc.kodi"
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :cond_custom_webpush

    const-string v2, "4355e037-d041-442f-b38a-3a31c0a91c7e"
    iput-object v2, v0, Lz1/h;->b:Ljava/lang/String;
    const v2, -15108398
    iput v2, v0, Lz1/h;->g:I
    const/4 v2, 0x1
    iput v2, v0, Lz1/h;->d:I
    goto :goto_custom_end

    :cond_custom_webpush
    # Default to 应用程序 (c28e1d23-4567-4890-abcd-ef0123456789)
    const-string v2, "c28e1d23-4567-4890-abcd-ef0123456789"
    iput-object v2, v0, Lz1/h;->b:Ljava/lang/String;

    const-string v2, "com.nextgen.webpush"
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :cond_custom_fb

    const v2, -8963627
    iput v2, v0, Lz1/h;->g:I
    const/4 v2, 0x0
    iput v2, v0, Lz1/h;->d:I
    goto :goto_custom_end

    :cond_custom_fb
    const-string v2, "com.droidlogic.FileBrower"
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :cond_custom_set

    const v2, -14705564
    iput v2, v0, Lz1/h;->g:I
    const/4 v2, 0x1
    iput v2, v0, Lz1/h;->d:I
    goto :goto_custom_end

    :cond_custom_set
    const-string v2, "com.android.settings"
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v2
    if-eqz v2, :cond_custom_atv

    const v2, -7697782
    iput v2, v0, Lz1/h;->g:I
    const/4 v2, 0x2
    iput v2, v0, Lz1/h;->d:I
    goto :goto_custom_end

    :cond_custom_atv
    const-string v2, "ca.dstudio.atvlauncher.pro"
    invoke-virtual {v1, v2}, Ljava/lang/String;->equals(Ljava/lang/Object;)Z
    move-result v1
    if-eqz v1, :cond_custom_default

    const v1, -13654050
    iput v1, v0, Lz1/h;->g:I
    const/4 v1, 0x3
    iput v1, v0, Lz1/h;->d:I
    goto :goto_custom_end

    :cond_custom_default
    const v1, -14314529
    iput v1, v0, Lz1/h;->g:I

    :goto_custom_end
"""

# Find return-object v0 in method c
new_lines = []
in_method_c = False
patched = False

for i, line in enumerate(lines):
    if ".method public static c(Landroid/content/Context;Landroid/content/ComponentName;)Lz1/a;" in line:
        in_method_c = True
    if in_method_c and not patched and line.strip() == "return-object v0":
        new_lines.append(patch_smali + "\n")
        new_lines.append(line)
        patched = True
        in_method_c = False
    else:
        new_lines.append(line)

with open(t1_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.writelines(new_lines)

print(f"[+] Successfully injected native auto-classification patch into t1/a.smali method c() (Patched: {patched})")
