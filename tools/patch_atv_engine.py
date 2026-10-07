import os

# 1. Patch z1/b.smali (Default Card Rounded Corners -> 16px)
b_smali = "tools/re_tools/atv_decompiled/smali/z1/b.smali"
with open(b_smali, 'r', encoding='utf-8') as f:
    b_content = f.read()

# Replace border-radius 8 with 16
b_content_patched = b_content.replace("const/16 v0, 0x8", "const/16 v0, 0x10")
with open(b_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.write(b_content_patched)
print("[+] Patched z1/b.smali border-radius -> 16px")

# 2. Patch y1/h.smali c()Lz1/d; method (Dual Sections: 影音播放 + 应用程序)
h_smali = "tools/re_tools/atv_decompiled/smali/y1/h.smali"
with open(h_smali, 'r', encoding='utf-8') as f:
    h_lines = f.readlines()

new_method = """# virtual methods
.method public c()Lz1/d;
    .locals 5

    # --- Section 1: 影音播放 ---
    new-instance v0, Lz1/d;
    invoke-direct {v0}, Lz1/d;-><init>()V

    const-string v1, "4355e037-d041-442f-b38a-3a31c0a91c7e"
    iput-object v1, v0, Lz1/d;->a:Ljava/lang/String;

    const-string v1, "影音播放"
    iput-object v1, v0, Lz1/d;->g:Ljava/lang/String;

    const/4 v1, 0x1
    iput-boolean v1, v0, Lz1/d;->h:Z
    iput v1, v0, Lz1/d;->i:I

    const/4 v2, 0x2
    iput v2, v0, Lz1/d;->b:I

    const/4 v3, 0x0
    iput-boolean v3, v0, Lz1/d;->d:Z
    iput-boolean v3, v0, Lz1/d;->c:Z
    iput-boolean v1, v0, Lz1/d;->e:Z

    const/4 v4, 0x5
    iput v4, v0, Lz1/d;->n:I
    iput v1, v0, Lz1/d;->m:I
    const/16 v4, 0x96
    iput v4, v0, Lz1/d;->l:I

    # --- Section 2: 应用程序 ---
    new-instance v1, Lz1/d;
    invoke-direct {v1}, Lz1/d;-><init>()V

    const-string v4, "c28e1d23-4567-4890-abcd-ef0123456789"
    iput-object v4, v1, Lz1/d;->a:Ljava/lang/String;

    const-string v4, "应用程序"
    iput-object v4, v1, Lz1/d;->g:Ljava/lang/String;

    const/4 v4, 0x1
    iput-boolean v4, v1, Lz1/d;->h:Z
    iput v2, v1, Lz1/d;->i:I
    iput v2, v1, Lz1/d;->b:I
    iput-boolean v4, v1, Lz1/d;->d:Z
    iput-boolean v3, v1, Lz1/d;->c:Z
    iput-boolean v4, v1, Lz1/d;->e:Z

    const/4 v2, 0x5
    iput v2, v1, Lz1/d;->n:I
    iput v4, v1, Lz1/d;->m:I
    const/16 v2, 0x96
    iput v2, v1, Lz1/d;->l:I

    # --- Insert both sections into Database ---
    const/4 v2, 0x2
    new-array v2, v2, [Lz1/d;
    aput-object v0, v2, v3
    aput-object v1, v2, v4

    move-object v0, p0
    check-cast v0, Ly1/i;
    invoke-virtual {v0, v2}, Ly1/i;->R([Lz1/d;)V

    # Return primary section (应用程序)
    return-object v1
.end method
"""

# Replace method c in y1/h.smali
start_idx = -1
end_idx = -1
for i, line in enumerate(h_lines):
    if line.strip() == ".method public c()Lz1/d;":
        start_idx = i
    if start_idx != -1 and line.strip() == ".end method":
        end_idx = i + 1
        break

if start_idx != -1 and end_idx != -1:
    h_lines = h_lines[:start_idx] + [new_method] + h_lines[end_idx:]
    with open(h_smali, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(h_lines)
    print("[+] Successfully replaced y1/h.smali c() method with Dual-Section Initializer!")
else:
    print("Warning: c() method not found in y1/h.smali")
