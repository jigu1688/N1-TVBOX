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

# Try to set text via am broadcast or input
# Let's test if we can type via broadcast or keyevents
# First, let's see if ADB Keyboard or similar exists, or if we can input characters
# On Android 7.1, we can use clipboard or input text
# Let's test typing "Media" or using clipboard
# First try: adb shell input text
subprocess.run([adb, '-s', dev, 'shell', 'am broadcast -a clipper.set -e text "影音播放" 2>/dev/null'])

# Let's test if we can send utf8 input via am broadcast or sogou
# Alternatively, we can use base64 / unicode
# Let's test typing
key('DPAD_DOWN', 0.3)
capture('add_sec_btn')
# Click "应用"
key('ENTER', 0.8)
capture('after_add_sec')
