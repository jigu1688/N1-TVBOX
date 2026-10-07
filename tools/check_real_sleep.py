import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
r = subprocess.run([adb, "-s", dev, "shell", "cat /seapp_contexts | grep -E 'priv|platform|system'"], capture_output=True, text=True)
print("seapp_contexts:\n", r.stdout[:1000])
