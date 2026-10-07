import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "busybox nc --help"], capture_output=True, text=True)
print("busybox nc help:\n", r.stdout, r.stderr)
