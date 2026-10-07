import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.115:5555'

# Let's test if supolicy allows entrypoint on shell_exec for su, or test running a test service
# We can check with supolicy --dumpav or sesearch if available
r = subprocess.run([adb, '-s', dev, 'shell', '/system/xbin/supolicy --dumpav | grep entrypoint | grep \" su \"'], capture_output=True, text=True)
print("su entrypoint rules:")
print(r.stdout[:1000] if r.stdout else "None or command failed")
