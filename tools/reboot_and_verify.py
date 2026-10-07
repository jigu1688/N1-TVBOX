import subprocess, time

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
dev = "192.168.31.115:5555"

print("[*] Rebooting box 192.168.31.115 to reload framework permissions...")
subprocess.run([adb, "-s", dev, "shell", "reboot"])

print("[*] Waiting 25 seconds for box to reboot...")
time.sleep(25)

connected = False
for i in range(20):
    print(f"[*] Attempting reconnect ({i+1}/20)...")
    r = subprocess.run([adb, "connect", dev], capture_output=True, text=True)
    if "connected to" in r.stdout:
        print("[+] Connected to box!")
        connected = True
        break
    time.sleep(3)

if connected:
    time.sleep(5)
    r = subprocess.run([adb, "-s", dev, "shell", "dumpsys package permission android.permission.DEVICE_POWER | head -n 10"], capture_output=True, text=True)
    print("=== DEVICE_POWER PERMISSION ON DEVICE ===")
    print(r.stdout.strip())
