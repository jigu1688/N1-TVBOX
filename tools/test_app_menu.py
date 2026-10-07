import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# 1. Focus on the first app in 应用程序 section
# Press Down to go to 应用程序 section
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 4']) # Clean dialog
time.sleep(0.5)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20']) # Down
time.sleep(0.3)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 20']) # Down to apps
time.sleep(0.5)

# Press Menu (Keyevent 82) to open App Menu
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'])
time.sleep(1)

# Screencap app menu
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/app_menu_check.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/app_menu_check.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\app_menu_check.png'])
