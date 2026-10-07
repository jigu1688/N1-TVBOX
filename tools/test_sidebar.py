import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# 1. Open ATV Sections list dialog
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82']) # Menu
time.sleep(1)
for _ in range(5):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20']) # Down to 桌面分区
    time.sleep(0.2)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 23']) # Enter
time.sleep(1)

# Now in 桌面分区 list:
# 1st item is 小组件. Press Right to focus on action or click it
# In ATV, pressing Menu on a section opens its settings!
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 19'])
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 19'])
time.sleep(0.5)

# Press Menu on 小组件 to open its sidebar
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/sec_widget_sidebar.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/sec_widget_sidebar.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\sec_widget_sidebar.png'])
