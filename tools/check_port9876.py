import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "netstat -tlpn || busybox netstat -tlpn || grep 9876 /proc/net/tcp"], capture_output=True, text=True)
print(r.stdout)
