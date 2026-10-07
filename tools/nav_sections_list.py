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

# Back to settings root
key('BACK', 0.5)

# Go to top item "分区"
for _ in range(5):
    key('DPAD_UP', 0.2)

capture('atv_settings_top')
key('ENTER', 0.8)
capture('atv_sections_list')
