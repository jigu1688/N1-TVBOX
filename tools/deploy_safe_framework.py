import subprocess, os

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

local_fw = os.path.abspath("build_rom/system_root/framework/framework-res.apk")
print(f"[*] Local framework-res.apk size: {os.path.getsize(local_fw)} bytes")

subprocess.run([adb, "connect", dev], check=True)
subprocess.run([adb, "-s", dev, "shell", "mount -o remount,rw /system"], check=True)

# Backup current framework-res on box if not exists
subprocess.run([adb, "-s", dev, "shell", "[ ! -f /system/framework/framework-res.apk.orig ] && cp /system/framework/framework-res.apk /system/framework/framework-res.apk.orig"])

print("[*] Pushing to /system/framework/framework-res.apk.new...")
subprocess.run([adb, "-s", dev, "push", local_fw, "/system/framework/framework-res.apk.new"], check=True)
subprocess.run([adb, "-s", dev, "shell", "chmod 644 /system/framework/framework-res.apk.new && chown 0:0 /system/framework/framework-res.apk.new"], check=True)

print("[*] Atomically moving into place...")
subprocess.run([adb, "-s", dev, "shell", "mv /system/framework/framework-res.apk.new /system/framework/framework-res.apk"], check=True)
subprocess.run([adb, "-s", dev, "shell", "sync"], check=True)

print("[+] Successfully replaced framework-res.apk on device!")
