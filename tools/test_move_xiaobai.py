import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Back to desktop
for _ in range(3):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4'])
    time.sleep(0.2)

# Home
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 3'])
time.sleep(1)

# Down to 应用程序
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.3)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.5)

# Focus on 小白 (last item in 应用程序) -> Right 4 times
for _ in range(4):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 22'])
    time.sleep(0.3)

# Open Menu
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

# Down 3 times to '移动到分区'
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
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/xiaobai_move.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/xiaobai_move.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\xiaobai_move.png'])
