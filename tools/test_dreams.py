import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"
subprocess.run([adb, "connect", dev], capture_output=True, timeout=5)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True, errors="replace", timeout=5).stdout.strip()

print("=== CHECK DREAM SERVICE ===")
# android.service.dreams.IDreamManager methods
# 1: dream(), 2: awaken(), 3: setDreamComponents(), 4: getDreamComponents(), 5: getDefaultDreamComponent(), 6: testDream(), 7: isDreaming(), 8: finishSelf(), 9: startDozing(), 10: stopDozing(), 11: forceAmbientDisplayNecessity()
print("service call dreams 1:", sh("service call dreams 1"))

print("=== CHECK DREAMS WAKEFULNESS ===")
print(sh("dumpsys power | grep -i wakefulness"))
