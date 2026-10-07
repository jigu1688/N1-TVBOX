import subprocess

debug_sig = '30820312308201faa003020102020900de1bb136fb132a88300d06092a864886f70d01010c05003036310b30090603550406130255533110300e060355040a1307416e64726f6964311530130603550403130c416e64726f696444656275673020170d3236303833303030303132345a180f32303534303131353030303132345a3036310b30090603550406130255533110300e060355040a1307416e64726f6964311530130603550403130c416e64726f6964446562756730820122300d06092a864886f70d01010105000382010f003082010a0282010100d47bd3c45454752cb001dc5c38a7ff09be27e10c5cc6a61f80797d36420f45c3438b0f02150313e6b109344e225949143f9cb2b00b970c60a9a3e54580e840acdcac9f8ef4ccf34f263c4d7dbdc9b50f6214712ca9da7cd04a9969cd84aaff3ea07724d97a33ae37fd8b2be9e17cb3beb52983e5ceb26b2f014f706bdd0e8be1c45ec70e8416489398d3d14d64b38c5ff1ee1e7cb5854fcf1c2323f43a9d0ebf794343908763091d73da4a166968334ff791f5956ba536515e7f6b42a4a30cc7a175d6d18976d4a053e79eb6f8083dd259c842d4e589ddac789987a7d1904e35f389ec88b13c5ce52dd32d86b62445755f019d4faa1edcdc2e12215c0fb414ef0203010001a321301f301d0603551d0e04160414547f4023cfc2e4cb471fff1769a267801c5abd74300d06092a864886f70d01010c050003820101005fe3dec7d2adb8d37fc8cb9aeff595f123b1984c4f7fc69d51c3ef187bb42c166abfeb8394961c5cde9a54e7eca227d8b63f3c5c4168354d87f3438f1b8d5201fa9ba0417b1822298124a391bbe140df67ae78c5e8e744264f10eda5def6cf01d7a375b84ee61b57930b974a43bf48790c692d3d0fb20cab433dd1e6e3160a51709df1fec643fef09f08534e4ec37e2eb216da0c358daf03081eb4795c2675c6128077e217065504027533449c75189454c773539fee3dfede9f384302025b740b999abb6945ecac5474cf9075886a3b5b24d647dd3c3694e52f10f06e48f053b897d164fe5d5c0d00822329363bb2f1228f34585fb348c135705fcdf1bf8960'

path = 'build_rom/system_root/etc/security/mac_permissions.xml'
with open(path, 'r', encoding='latin1') as f:
    c = f.read()

if debug_sig not in c:
    new_signer = f'<signer signature="{debug_sig}"><seinfo value="platform"/></signer>'
    c = c.replace('</policy>', new_signer + '</policy>')
    with open(path, 'w', encoding='latin1') as f:
        f.write(c)
    print('[*] Updated build_rom mac_permissions.xml')
else:
    print('[*] Already present in build_rom mac_permissions.xml')

# Also push to box if online
adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.111:5555"
subprocess.run([adb, "connect", dev], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([adb, "-s", dev, "shell", "mount -o remount,rw /system"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.run([adb, "-s", dev, "push", path, "/system/etc/security/mac_permissions.xml"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 644 /system/etc/security/mac_permissions.xml"], check=True)
print('[*] Pushed updated mac_permissions.xml to box')
