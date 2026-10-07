import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "dumpsys package com.android.tv.settings | grep -i privateFlags"], capture_output=True, text=True)
print("TvSettings privateFlags:\n", r.stdout)
r2 = subprocess.run([adb, "-s", dev, "shell", "dumpsys package com.android.systemui | grep -i privateFlags"], capture_output=True, text=True)
print("SystemUI privateFlags:\n", r2.stdout)
