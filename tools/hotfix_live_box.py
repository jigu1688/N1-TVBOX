import subprocess
import time

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

subprocess.run([adb, 'connect', dev], capture_output=True)

print("[*] Remounting /system...")
subprocess.run([adb, '-s', dev, 'shell', 'mount -o remount,rw /system'], capture_output=True)

print("[*] Pushing clean framework-res.apk to device...")
subprocess.run([adb, '-s', dev, 'push', 'build_rom/system_root/framework/framework-res.apk', '/system/framework/framework-res.apk'], capture_output=True)

subprocess.run([adb, '-s', dev, 'shell', 'chmod 644 /system/framework/framework-res.apk'], capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 'chown 0:0 /system/framework/framework-res.apk'], capture_output=True)

print("[*] Rebooting Android framework...")
subprocess.run([adb, '-s', dev, 'shell', 'setprop ctl.restart zygote'], capture_output=True)

time.sleep(8)
print("[+] Finished hotfix push!")
