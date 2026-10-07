import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Back to clean
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4'])
time.sleep(0.5)

# Menu -> 桌面分区
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)
for _ in range(5):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20'])
    time.sleep(0.2)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23'])
time.sleep(1)

# Now in 桌面分区 dialog:
# Focus on 1st item '小组件'
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 19'])
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 19'])
time.sleep(0.5)

# Click on '小组件' (DPAD_CENTER = 23)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23'])
time.sleep(1)

subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/sec_widget_click.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/sec_widget_click.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\sec_widget_click.png'])
