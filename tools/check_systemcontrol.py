import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"
subprocess.run([adb, "connect", dev], capture_output=True, timeout=5)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace", timeout=5).stdout.strip()

print(sh("strings /system/bin/systemcontrol | grep -n -E 'Sysfs|Bootenv|Mode'"))
