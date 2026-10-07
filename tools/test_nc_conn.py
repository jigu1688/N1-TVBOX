import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "echo '' | /system/xbin/busybox nc 127.0.0.1 19999"], capture_output=True, text=True)
print("nc connect result:\n", r.stdout, r.stderr)
