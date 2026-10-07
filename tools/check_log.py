import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "logcat", "-d", "-t", "80"], capture_output=True, text=True, encoding="utf-8", errors="replace")
for line in r.stdout.splitlines():
    if any(k in line for k in ["ShutdownActivity", "PowerManager", "power", "sleep", "goToSleep", "ArcView"]):
        print(line)
