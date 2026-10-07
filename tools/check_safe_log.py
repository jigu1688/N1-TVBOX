import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "logcat", "-d", "-s", "SafeSleepManager:V"], capture_output=True, text=True, encoding="utf-8", errors="replace")
print(r.stdout)
