import subprocess
import os
import sys

def push_and_verify():
    adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    dev = "192.168.31.118:5555"
    apk_local = os.path.abspath("build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk")
    apk_remote = "/system/priv-app/PhiTvSettings/PhiTvSettings.apk"

    print(f"[*] Local APK size: {os.path.getsize(apk_local)} bytes")

    # 0. Connect device
    print(f"[*] Connecting to {dev}...")
    r = subprocess.run([adb, "connect", dev], capture_output=True, text=True)
    print("    connect output:", r.stdout.strip())

    print("[*] Remounting /system as rw...")
    r = subprocess.run([adb, "-s", dev, "shell", "mount -o remount,rw /system"], capture_output=True, text=True)
    print("    mount result:", r.stdout.strip(), r.stderr.strip())

    # 2. Check remote dir
    subprocess.run([adb, "-s", dev, "shell", "mkdir -p /system/priv-app/PhiTvSettings"], check=True)

    # 3. Push APK
    print(f"[*] Pushing to {apk_remote}...")
    r = subprocess.run([adb, "-s", dev, "push", apk_local, apk_remote], capture_output=True, text=True)
    print("    push output:", r.stdout.strip())
    if r.returncode != 0:
        print("[!] Push failed:", r.stderr.strip())
        return False

    # 4. Set permissions
    print("[*] Setting chmod 644 and chown 0:0...")
    subprocess.run([adb, "-s", dev, "shell", f"chmod 644 {apk_remote}"], check=True)
    subprocess.run([adb, "-s", dev, "shell", f"chown 0:0 {apk_remote}"], check=True)

    # 5. Verify size on device
    r = subprocess.run([adb, "-s", dev, "shell", f"ls -l {apk_remote}"], capture_output=True, text=True)
    print("    Remote file:", r.stdout.strip())

    # 6. Stop old process so it reloads
    print("[*] Stopping com.android.tv.settings process...")
    subprocess.run([adb, "-s", dev, "shell", "am force-stop com.android.tv.settings"], check=True)

    # 7. Also test install -r -d if necessary or check pm path
    r = subprocess.run([adb, "-s", dev, "shell", "pm path com.android.tv.settings"], capture_output=True, text=True)
    print("    Package manager path:", r.stdout.strip())

    print("[+] Successfully updated PhiTvSettings.apk on 192.168.31.111!")
    return True

if __name__ == "__main__":
    push_and_verify()
