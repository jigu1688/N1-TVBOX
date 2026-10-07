import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Clean screen
for _ in range(3):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4'])
    time.sleep(0.2)

# Focus on SeleneTV (2nd item in 应用程序)
# Down twice
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.3)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.5)

# Press Right to SeleneTV
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 22'])
time.sleep(0.5)

# Menu
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

# Down to '移动到分区' (4th item in app menu: 移动, 配置, 卸载, 移动到分区)
for _ in range(3):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
    time.sleep(0.3)

# Enter on '移动到分区'
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23'])
time.sleep(1)

# Enter on '影音播放'
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23'])
time.sleep(2)

# Screencap
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/selenetv_moved_live.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/selenetv_moved_live.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\selenetv_moved_live.png'])
