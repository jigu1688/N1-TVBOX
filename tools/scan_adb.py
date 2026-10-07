import subprocess, ipaddress, concurrent.futures

adb = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"

def test_ip(ip):
    r = subprocess.run([adb, "connect", f"{ip}:5555"], capture_output=True, text=True, timeout=2)
    if "connected to" in r.stdout:
        return f"{ip}:5555"
    return None

# Try known IPs first
for ip in ["192.168.31.115", "192.168.31.111", "10.0.0.102", "10.0.0.100", "10.0.0.101"]:
    try:
        res = test_ip(ip)
        if res:
            print(f"[+] FOUND ADB at {res}")
            exit(0)
    except:
        pass

# Scan 10.0.0.0/24
print("[*] Scanning 10.0.0.x for ADB 5555...")
with concurrent.futures.ThreadPoolExecutor(max_workers=30) as ex:
    futures = {ex.submit(test_ip, f"10.0.0.{i}"): i for i in range(2, 255)}
    for f in concurrent.futures.as_completed(futures):
        try:
            res = f.result()
            if res:
                print(f"[+] FOUND ADB at {res}")
                exit(0)
        except:
            pass

print("[-] No ADB found on 10.0.0.x")
