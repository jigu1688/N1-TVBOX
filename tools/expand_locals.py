impl_smali = "tools/re_tools/atv_decompiled/smali/ca/dstudio/atvlauncher/room/database/LauncherDatabase_Impl$a.smali"

with open(impl_smali, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace .locals 1 in method a with .locals 4
c = c.replace(".method public final a(Ld1/b;)V\n    .locals 1",
              ".method public final a(Ld1/b;)V\n    .locals 4")

with open(impl_smali, 'w', encoding='utf-8', newline='\n') as f:
    f.write(c)

print("[+] Successfully expanded locals in method a(Ld1/b;)V from 1 to 4!")
