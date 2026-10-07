import subprocess, time, sys
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Navigate to ATV Settings -> Launcher Settings
# From the menu screenshot, "启动器设置" is the second to last item
# Menu items: 移动, 配置, 应用程序信息, 创建文件夹, 桌面分区, 启动器设置, 安卓设置

# Go HOME first
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_HOME'])
time.sleep(1)

# Open menu
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_MENU'])
time.sleep(1)

# Navigate down to "启动器设置" (5 times from top)
for i in range(5):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_DPAD_DOWN'])
    time.sleep(0.5)

# Take screenshot to see current position
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/atv_nav1.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_nav1.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_nav1.png'])

# Select it
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_ENTER'])
time.sleep(2)

# Screenshot launcher settings
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/atv_launcher_settings.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_launcher_settings.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_launcher_settings.png'])

print('Done - check screenshots')
