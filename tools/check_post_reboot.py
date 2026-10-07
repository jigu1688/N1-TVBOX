import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

def run(cmd):
    subprocess.run([adb, 'connect', dev], capture_output=True, text=True)
    r = subprocess.run([adb, '-s', dev, 'shell', cmd], capture_output=True, text=True)
    return r.stdout

print("=== PS ===")
print(run("ps | grep -E 'busybox|nc|sleep|webpad'"))

print("=== NETSTAT ===")
print(run("netstat -tlpn"))

print("=== LOGCAT WEBPAD ===")
print(run("logcat -d | grep -i webpad"))

print("=== INIT SERVICES ===")
print(run("getprop | grep init.svc"))
