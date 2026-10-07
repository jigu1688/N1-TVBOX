import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

subprocess.run([adb, "connect", dev], stdout=subprocess.DEVNULL)
time.sleep(1)

def sh(cmd):
    return subprocess.run([adb, "-s", dev, "shell", cmd], capture_output=True, text=True).stdout.strip()

nodes = ['osd_name', 'physical_addr', 'pin_status', 'port_status', 'wake_up', 'cec_version', 'fun_cfg', 'device_type']
for n in nodes:
    print(f"{n}: {sh(f'cat /sys/class/aocec/{n}')}")

print("dumpsys hdmi_control summary:")
print(sh("dumpsys hdmi_control | head -n 25"))
