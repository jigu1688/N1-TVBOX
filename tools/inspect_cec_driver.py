import subprocess

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

def ensure_conn():
    subprocess.run([adb, "connect", dev], stdout=subprocess.DEVNULL)

def sh(cmd):
    ensure_conn()
    r = subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True)
    return r.stdout.strip()

print("1. Settings.Global values:")
print("   hdmi_control_enabled:", sh("settings get global hdmi_control_enabled"))
print("   hdmi_control_auto_device_off_enabled:", sh("settings get global hdmi_control_auto_device_off_enabled"))
print("   hdmi_control_auto_wakeup_enabled:", sh("settings get global hdmi_control_auto_wakeup_enabled"))

print("\n2. Devices in /dev:")
print(sh("ls -la /dev | grep -i cec"))

print("\n3. Class cec sysfs:")
print(sh("ls -la /sys/class/aocec /sys/class/cec 2>/dev/null"))

print("\n4. Dmesg CEC logs:")
logs = sh("dmesg")
cec_logs = [l for l in logs.splitlines() if any(k in l.lower() for k in ["cec", "hdmitx"])]
for l in cec_logs[:25]:
    print("  ", l)

print("\n5. Dumpsys hdmi_control detail:")
print(sh("dumpsys hdmi_control"))
