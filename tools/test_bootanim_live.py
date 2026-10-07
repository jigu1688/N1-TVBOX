import subprocess, time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.118:5555'

subprocess.run([adb, 'connect', dev])
time.sleep(1)

print('[*] Starting /system/bin/bootanimation on screen for 5 seconds...')
proc = subprocess.Popen([adb, '-s', dev, 'shell', 'su', '-c', '/system/bin/bootanimation'])
time.sleep(2)

print('[*] Capturing screen...')
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/anim_cap.png'])
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/anim_cap.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\3a664381-8939-4916-9404-683857cb0b2a\live_bootanim_screen.png'])

time.sleep(1)
print('[*] Stopping bootanimation...')
subprocess.run([adb, '-s', dev, 'shell', 'su', '-c', 'pkill -9 bootanimation || killall bootanimation'])
proc.terminate()
print('[+] Test completed!')
