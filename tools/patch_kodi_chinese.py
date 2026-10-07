import zipfile
import os
import shutil

def patch_kodi_chinese():
    src_apk = 'tools/Kodi_19.5_Matrix_arm64.apk'
    dst_apk = 'tools/Kodi_19.5_Matrix_arm64_zh.apk'
    
    print("[*] Repacking Kodi 19.5 with built-in Simplified Chinese & Arial font...")
    
    # 1. Read existing APK
    with zipfile.ZipFile(src_apk, 'r') as zin:
        settings_xml = zin.read('assets/system/settings/settings.xml').decode('utf-8')
        
        # Patch default font to Arial
        settings_xml = settings_xml.replace(
            '<setting id="lookandfeel.font" type="string" parent="lookandfeel.skin" label="13303" help="36107">\n            <level>0</level>\n            <default>Default</default>',
            '<setting id="lookandfeel.font" type="string" parent="lookandfeel.skin" label="13303" help="36107">\n            <level>0</level>\n            <default>Arial</default>'
        )
        # In case indentation varies:
        settings_xml = settings_xml.replace(
            '<setting id="lookandfeel.font" type="string" parent="lookandfeel.skin"',
            '<!-- patched font -->\n          <setting id="lookandfeel.font" type="string" parent="lookandfeel.skin"'
        ).replace(
            '<setting id="locale.language" type="addon" label="248" help="36114">\n            <level>0</level>\n            <default>resource.language.en_gb</default>',
            '<setting id="locale.language" type="addon" label="248" help="36114">\n            <level>0</level>\n            <default>resource.language.zh_cn</default>'
        )
        
        # If replace didn't match exact indentation, use regex or direct string replace
        if '<default>resource.language.zh_cn</default>' not in settings_xml:
            import re
            settings_xml = re.sub(
                r'(<setting id="locale\.language"[^>]*>[\s\S]*?<default>)resource\.language\.en_gb(</default>)',
                r'\g<1>resource.language.zh_cn\g<2>',
                settings_xml
            )
            settings_xml = re.sub(
                r'(<setting id="lookandfeel\.font"[^>]*>[\s\S]*?<default>)Default(</default>)',
                r'\g<1>Arial\g<2>',
                settings_xml
            )
            
        print("[*] settings.xml patched! Checked zh_cn in xml:", 'resource.language.zh_cn' in settings_xml)
        print("[*] settings.xml patched! Checked Arial in xml:", 'Arial' in settings_xml)
        
        # 2. Write new zip
        with zipfile.ZipFile(dst_apk, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'assets/system/settings/settings.xml':
                    zout.writestr(item, settings_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
            # 3. Add resource.language.zh_cn
            with open('tools/resource.language.zh_cn/addon.xml', 'rb') as f:
                zout.writestr('assets/addons/resource.language.zh_cn/addon.xml', f.read())
            with open('tools/resource.language.zh_cn/resources/strings.po', 'rb') as f:
                zout.writestr('assets/addons/resource.language.zh_cn/resources/strings.po', f.read())
                
    print("[+] Generated Chinese Kodi APK:", dst_apk, os.path.getsize(dst_apk), "bytes")

if __name__ == '__main__':
    patch_kodi_chinese()
