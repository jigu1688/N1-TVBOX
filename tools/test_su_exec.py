import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
# Test running su as uid 10010
r = subprocess.run([adb, "-s", dev, "shell", "run-as com.android.tv.settings su -c id || su -c id"], capture_output=True, text=True)
print("Result of su id:", r.stdout.strip(), r.stderr.strip())
