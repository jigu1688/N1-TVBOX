import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

def key(k, delay=0.5):
    subprocess.run([adb, '-s', dev, 'shell', f'input keyevent KEYCODE_{k}'])
    time.sleep(delay)

def capture(name):
    subprocess.run([adb, '-s', dev, 'shell', f'screencap -p /sdcard/{name}.png'])
    subprocess.run([adb, '-s', dev, 'pull', f'/sdcard/{name}.png', 
                    f'C:\\Users\\jigu\\.gemini\antigravity-ide\\brain\\59392cea-4993-4618-813e-365af128b445\\{name}.png'])

# 1. Back to Home
key('BACK', 0.5)
key('BACK', 0.5)
key('HOME', 1)

# 2. Select 乐播投屏 (DPAD_RIGHT from ATV桌面)
key('DPAD_RIGHT', 0.5)
capture('selected_hpplay')

# 3. Press MENU
key('MENU', 0.8)
capture('hpplay_menu')
