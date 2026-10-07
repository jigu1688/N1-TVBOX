import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.118:5555"

subprocess.run([adb, "connect", dev], check=True)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace").stdout.strip()

print("Current wakefulness:", sh("dumpsys power | grep -i wakefulness"))

# Check who owns input binary
print("ls -l /system/bin/input:", sh("ls -l /system/bin/input"))

# Test running input keyevent 223 via adb shell
print("adb shell input keyevent 223 test:")
print(sh("input keyevent 223"))

print("After keyevent wakefulness:", sh("dumpsys power | grep -i wakefulness"))

# Wake it back up
print("Waking up:", sh("input keyevent 224"))
print("Restored wakefulness:", sh("dumpsys power | grep -i wakefulness"))
