import subprocess
import os

def setup_kodi_chinese():
    adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    target = "192.168.31.117:5555"
    
    print("[*] Pushing resource.language.zh_cn addon to Kodi...")
    subprocess.run([adb, "-s", target, "shell", "mkdir", "-p", "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/resource.language.zh_cn"], check=True)
    subprocess.run([adb, "-s", target, "push", "tools/resource.language.zh_cn/.", "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/addons/resource.language.zh_cn/"], check=True)
    
    print("[*] Pulling guisettings.xml...")
    subprocess.run([adb, "-s", target, "pull", "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/guisettings.xml", "tools/guisettings.xml"], check=True)
    
    with open("tools/guisettings.xml", "r", encoding="utf-8") as f:
        content = f.read()
        
    inject = """    <setting id="locale.language">resource.language.zh_cn</setting>
    <setting id="lookandfeel.font">Arial</setting>
    <setting id="locale.charset">CP936</setting>
    <setting id="locale.country">China</setting>
"""
    if "</settings>" in content:
        content = content.replace("</settings>", inject + "</settings>")
        
    with open("tools/guisettings.xml", "w", encoding="utf-8") as f:
        f.write(content)
        
    print("[*] Pushing updated guisettings.xml...")
    subprocess.run([adb, "-s", target, "push", "tools/guisettings.xml", "/sdcard/Android/data/org.xbmc.kodi/files/.kodi/userdata/guisettings.xml"], check=True)
    
    print("[*] Restarting Kodi...")
    subprocess.run([adb, "-s", target, "shell", "am", "force-stop", "org.xbmc.kodi"], check=True)
    subprocess.run([adb, "-s", target, "shell", "am", "start", "-n", "org.xbmc.kodi/.Main"], check=True)
    print("[+] Done!")

if __name__ == '__main__':
    setup_kodi_chinese()
