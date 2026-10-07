import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Back to desktop
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4'])
time.sleep(1)

# Focus on SeleneTV or 千寻
# Press Home
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 3'])
time.sleep(1)

# Down to 应用程序
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.3)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.5)

# Open App Menu on 1st item
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

# Tap directly on "移动到分区" (x=1600, y=470)
subprocess.run([adb, '-s', dev, 'shell', 'input tap 1600 470'])
time.sleep(1)

# Tap on "影音播放" (x=1600, y=200)
subprocess.run([adb, '-s', dev, 'shell', 'input tap 1600 200'])
time.sleep(2)

# Screencap
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/move_success_verified.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/move_success_verified.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\move_success_verified.png'])
