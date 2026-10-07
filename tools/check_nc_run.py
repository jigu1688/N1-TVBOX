import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], capture_output=True, timeout=5)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace", timeout=5).stdout.strip()

print("busybox nc matches:", sh("/system/xbin/busybox --list | grep nc"))
print("busybox telnet matches:", sh("/system/xbin/busybox --list | grep telnet"))
print("busybox http matches:", sh("/system/xbin/busybox --list | grep http"))
print("which nc:", sh("which nc"))
