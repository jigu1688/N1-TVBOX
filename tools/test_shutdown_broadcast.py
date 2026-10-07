import subprocess

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.103:5555'

# Test sending ACTION_REQUEST_SHUTDOWN broadcast
# In Android 7.1.2:
# sendBroadcast(new Intent("android.intent.action.ACTION_REQUEST_SHUTDOWN").putExtra("android.intent.extra.KEY_CONFIRM", false).setFlags(Intent.FLAG_ACTIVITY_NEW_TASK));
print("[*] Testing ACTION_REQUEST_SHUTDOWN broadcast...")
p = subprocess.run([adb, '-s', dev, 'shell', 'am broadcast -a android.intent.action.ACTION_REQUEST_SHUTDOWN --ez android.intent.extra.KEY_CONFIRM false'], capture_output=True)
print("stdout:", p.stdout.decode('utf-8', errors='ignore'))
print("stderr:", p.stderr.decode('utf-8', errors='ignore'))
