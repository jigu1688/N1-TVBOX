import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Clean screen
for _ in range(3):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4'])
    time.sleep(0.2)

# Focus on SeleneTV (which is at position 0 in 应用程序 section)
# Down to 应用程序
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.3)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.5)

# Press Menu to open App Menu
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

# Down to '移动到分区' (position 4 in app menu: 移动, 配置, 卸载, 移动到分区)
for _ in range(3):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
    time.sleep(0.3)

# Enter to open '选择分区'
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23'])
time.sleep(1)

# In '选择分区', the only other section is '影音播放'. Press Enter!
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23'])
time.sleep(2)

# Capture screen
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/move_to_section_verified.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/move_to_section_verified.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\move_to_section_verified.png'])
