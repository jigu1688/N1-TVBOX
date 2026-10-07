import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "pm grant com.android.tv.settings android.permission.DEVICE_POWER"], capture_output=True, text=True)
print("pm grant result:\n", r.stdout, r.stderr)
