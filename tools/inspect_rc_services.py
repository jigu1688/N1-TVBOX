import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    r = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, text=True)
    return r.stdout

print("=== SERVICES in /init.rc ===")
out = run("cat /init.rc")
for line in out.splitlines():
    if line.startswith("service ") or "seclabel" in line:
        print("  ", line)

print("=== SERVICES in /init.*.rc ===")
out2 = run("cat /init.*.rc")
for line in out2.splitlines():
    if line.startswith("service ") or "seclabel" in line:
        print("  ", line)
