import subprocess
import time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.111:5555"

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

print("1. Launching DisplayActivity...")
sh("am start -n com.android.tv.settings/.display.DisplayActivity")
time.sleep(2)

print("2. Focus HDMI resolution and move right to list...")
sh("input keyevent 22") # Right to list
time.sleep(0.5)

print("3. Move to 1080P 60Hz (UP)...")
sh("input keyevent 19") # UP to 1080p60hz
time.sleep(0.5)

print("4. Press ENTER on 1080P 60Hz...")
sh("input keyevent 23")
time.sleep(1.5)

print("5. Current mode:", sh("cat /sys/class/display/mode"))

# In confirm dialog: Cancel is focused by default, RIGHT moves to Confirm, then press ENTER!
print("6. Move to 'Confirm' button (RIGHT) and press ENTER...")
sh("input keyevent 22") # Focus 'Confirm'
time.sleep(0.5)
sh("input keyevent 23") # Click 'Confirm'
time.sleep(1)

print("7. Mode after confirm:", sh("cat /sys/class/display/mode"))

# Screencap
sh("screencap -p /sdcard/confirmed.png")
subprocess.run([adb, "-s", dev, "pull", "/sdcard/confirmed.png", "tools/confirmed.png"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("8. Screenshot saved to tools/confirmed.png")
