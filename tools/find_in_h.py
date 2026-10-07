import re

with open('tools/re_tools/libsystemcontrolservice.so', 'rb') as f:
    data = f.read()

# Let's search for strings like writeSysfs or method names
matches = re.findall(b'[a-zA-Z0-9_]{3,40}', data)
print("Unique strings with Sysfs/Bootenv/Mode/Sleep/Power:")
for m in sorted(set(matches)):
    ms = m.decode('ascii', errors='ignore')
    if any(k in ms.lower() for k in ['sysfs', 'sleep', 'power', 'standby', 'suspend', 'keyevent', 'bootenv']):
        print(" ", ms)
