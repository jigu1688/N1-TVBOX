import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], check=True)
# List classes in droidlogic or phicommcore
r = subprocess.run([adb, "-s", dev, "shell", "dexdump -c /system/framework/droidlogic.jar | grep 'Class descriptor' | grep -i power"], capture_output=True, text=True)
print("droidlogic power classes:\n", r.stdout)
r2 = subprocess.run([adb, "-s", dev, "shell", "dexdump -c /system/framework/phicommcore.jar | grep 'Class descriptor'"], capture_output=True, text=True)
print("phicommcore classes:\n", r2.stdout)
