import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

def key(k, delay=0.5):
    subprocess.run([adb, '-s', dev, 'shell', f'input keyevent KEYCODE_{k}'])
    time.sleep(delay)

def capture(name):
    subprocess.run([adb, '-s', dev, 'shell', f'screencap -p /sdcard/{name}.png'])
    subprocess.run([adb, '-s', dev, 'pull', f'/sdcard/{name}.png', 
                    rf'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\{name}.png'])

# 1. Back out completely to home
key('BACK', 0.5)
key('BACK', 0.5)
key('BACK', 0.5)
key('HOME', 1)

# 2. Open main context menu
key('MENU', 1)
capture('menu_from_home')

# 3. Navigate down to "桌面分区" (4 down)
for _ in range(4):
    key('DPAD_DOWN', 0.3)
capture('selected_section_mgr')

key('ENTER', 1)
capture('section_mgr_page')
