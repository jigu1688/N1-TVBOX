import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# 1. Back to desktop
for _ in range(3):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4'])
    time.sleep(0.2)

# 2. Home
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 3'])
time.sleep(1)

# 3. Down twice to 应用程序
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.3)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
time.sleep(0.5)

# 4. Open Menu
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

# Screencap menu
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/menu1.png'])

# 5. Tap on '移动到分区' (1600, 470)
subprocess.run([adb, '-s', dev, 'shell', 'input tap 1600 470'])
time.sleep(1)

# Screencap section picker
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/picker.png'])

# 6. Tap on '影音播放' (1600, 150)
subprocess.run([adb, '-s', dev, 'shell', 'input tap 1600 150'])
time.sleep(2)

# Screencap final
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/final_moved.png'])

subprocess.run([adb, '-s', dev, 'pull', '/sdcard/menu1.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\menu1.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/picker.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\picker.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/final_moved.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\final_moved.png'])

res = subprocess.run([adb, '-s', dev, 'logcat', '-d', '-s', 'ATV_DEBUG:V'], capture_output=True, text=True)
print('=== LOGCAT ===\n', res.stdout)
