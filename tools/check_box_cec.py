import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

def ensure_conn():
    for _ in range(3):
        r = subprocess.run([adb, "connect", dev], capture_output=True, text=True)
        if "connected" in r.stdout or "already connected" in r.stdout:
            break
        time.sleep(1)

def sh(cmd):
    ensure_conn()
    r = subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True)
    return r.stdout.strip()

print("=== 1. Check services with hdmi / cec ===")
print(sh("service list | grep -i -E 'hdmi|cec'"))

print("=== 2. Check dumpsys hdmi_control ===")
print(sh("dumpsys hdmi_control"))

print("=== 3. Check sysfs amhdmitx cec nodes ===")
print(sh("ls -la /sys/class/amhdmitx/amhdmitx0/"))

print("=== 4. Check CEC properties ===")
print(sh("getprop | grep -i -E 'cec|hdmi'"))

print("=== 5. Check EDID CEC / physical address ===")
print(sh("cat /sys/class/amhdmitx/amhdmitx0/edid"))
