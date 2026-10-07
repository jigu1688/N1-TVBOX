manifest_path = r'tools/re_tools/tvsettings_decompiled/AndroidManifest.xml'
with open(manifest_path, 'r', encoding='utf-8') as f:
    mf = f.read()

target = '<uses-permission android:name="android.permission.DEVICE_POWER"/>'
replacement = '<uses-permission android:name="android.permission.DEVICE_POWER"/>\n    <uses-permission android:name="android.permission.WRITE_DREAM_STATE"/>\n    <uses-permission android:name="android.permission.READ_DREAM_STATE"/>'

new_mf = mf.replace(target, replacement)
with open(manifest_path, 'w', encoding='utf-8') as f:
    f.write(new_mf)

print('[+] Injected WRITE_DREAM_STATE & READ_DREAM_STATE into tvsettings AndroidManifest.xml')
