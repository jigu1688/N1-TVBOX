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

# 1. Focus back on input field
key('DPAD_UP', 0.5)

# 2. Type "Media"
subprocess.run([adb, '-s', dev, 'shell', 'input text "Media"'])
time.sleep(0.5)
capture('typed_media')

# 3. Focus on "应用"
key('DPAD_DOWN', 0.3)
capture('focus_apply_btn')

# 4. Click "应用"
key('ENTER', 1)
capture('after_create_media_sec')
