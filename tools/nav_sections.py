import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

def key(k, delay=0.5):
    subprocess.run([adb, '-s', dev, 'shell', f'input keyevent KEYCODE_{k}'])
    time.sleep(delay)

def capture(name):
    subprocess.run([adb, '-s', dev, 'shell', f'screencap -p /sdcard/{name}.png'])
    subprocess.run([adb, '-s', dev, 'pull', f'/sdcard/{name}.png', 
                    f'C:\\Users\\jigu\\.gemini\\antigravity-ide\\brain\\59392cea-4993-4618-813e-365af128b445\\{name}.png'])

# 1. Back to Home
key('HOME', 1)

# 2. Open Menu
key('MENU', 1)

# 3. Navigate down to "桌面分区" (4 times from top)
for _ in range(4):
    key('DPAD_DOWN', 0.3)

capture('atv_section_menu')
key('ENTER', 1)
capture('atv_section_page')
