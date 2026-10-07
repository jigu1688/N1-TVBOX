import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Disable Keyguard & Lockscreen
print("[*] Dismissing and disabling Keyguard...")
subprocess.run([adb, '-s', dev, 'shell', 'wm dismiss-keyguard'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'settings put secure lockscreen.disabled 1'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'settings put global device_provisioned 1'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'settings put secure user_setup_complete 1'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 82'], capture_output=True) # MENU / UNLOCK
subprocess.run([adb, '-s', dev, 'shell', 'input keyevent 3'], capture_output=True) # HOME

time.sleep(2)
subprocess.run([adb, '-s', dev, 'shell', 'screencap -p /sdcard/screen_unlocked.png'], capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/sdcard/screen_unlocked.png', 'tools/screen_unlocked.png'], capture_output=True)
print("[+] Captured tools/screen_unlocked.png")
