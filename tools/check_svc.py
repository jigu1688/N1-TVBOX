import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "cat /system/bin/svc"], capture_output=True, text=True)
print("Content of /system/bin/svc:")
print(r.stdout)
