import subprocess
import os
import time

def main():
    adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
    dev = "192.168.31.115:5555"
    apk_local = os.path.abspath("build_rom/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk")
    apk_remote = "/system/priv-app/PhiTvSettings/PhiTvSettings.apk"

    print(f"[*] Local APK size: {os.path.getsize(apk_local)} bytes")

    print(f"[*] Connecting to {dev}...")
    subprocess.run([adb, "connect", dev], check=True)

    print("[*] Remounting /system as rw...")
    subprocess.run([adb, "-s", dev, "shell", "mount -o remount,rw /system"], check=True)

    print(f"[*] Pushing to {apk_remote}...")
    subprocess.run([adb, "-s", dev, "push", apk_local, apk_remote], check=True)
    subprocess.run([adb, "-s", dev, "shell", f"chmod 644 {apk_remote}"], check=True)
    subprocess.run([adb, "-s", dev, "shell", f"chown 0:0 {apk_remote}"], check=True)

    print("[*] Force stopping old process...")
    subprocess.run([adb, "-s", dev, "shell", "am force-stop com.android.tv.settings"], check=True)

    r = subprocess.run([adb, "-s", dev, "shell", f"ls -l {apk_remote}"], capture_output=True, text=True)
    print("    Remote file:", r.stdout.strip())

    print("[+] Push complete!")

if __name__ == "__main__":
    main()
