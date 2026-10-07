import subprocess, time, sys
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Navigate to "备份和还原" from current settings page
# Current items: 分区, 壁纸, 隐藏的应用程序, 状态栏, 备份和还原
# We need to go down 4 times to reach "备份和还原"
for i in range(4):
    subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_DPAD_DOWN'])
    time.sleep(0.3)

# Screenshot to verify position
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/atv_backup_pos.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_backup_pos.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_backup_pos.png'])

# Select "备份和还原"
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent KEYCODE_ENTER'])
time.sleep(2)

# Screenshot backup page
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/atv_backup_page.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/atv_backup_page.png', 
    r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\atv_backup_page.png'])

print('Done - check backup page screenshot')
