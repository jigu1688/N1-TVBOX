import os, subprocess, glob

aapts = glob.glob(r"C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\*\aapt.exe")
aapt = aapts[0]

apk = os.path.abspath("build_rom/system_root/framework/framework-res.apk")
r = subprocess.run([aapt, "dump", "xmltree", apk, "AndroidManifest.xml"], capture_output=True, text=True, errors="replace")
lines = r.stdout.splitlines()
for i, line in enumerate(lines):
    if "DEVICE_POWER" in line or "INJECT_EVENTS" in line:
        for j in range(max(0, i-2), min(len(lines), i+6)):
            print(lines[j])
        print("---")
