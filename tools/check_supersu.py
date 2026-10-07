import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "ls -d /data/data/*supersu* /data/system/supersu* /system/app/*SuperSU* /system/priv-app/*SuperSU* 2>/dev/null"], capture_output=True, text=True)
print("SuperSU paths:\n", r.stdout)
