import subprocess
import socket
import sys

ADB = r"C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe"
TARGET_IP = "192.168.31.111"

def check_ping(ip):
    r = subprocess.run(f"ping -n 1 -w 1000 {ip}", shell=True, capture_output=True, text=True)
    return "TTL=" in r.stdout

def check_port(ip, port, timeout=2):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((ip, port))
        s.close()
        return True
    except Exception as e:
        return False

print(f"[*] Checking ping to {TARGET_IP}...")
print(f"    Ping reachable: {check_ping(TARGET_IP)}")

print(f"[*] Checking TCP port 5555 (ADB) on {TARGET_IP}...")
print(f"    Port 5555 open: {check_port(TARGET_IP, 5555)}")

print(f"[*] Checking TCP port 19999 (sleep daemon) on {TARGET_IP}...")
print(f"    Port 19999 open: {check_port(TARGET_IP, 19999)}")

print(f"[*] Checking TCP port 2323 (telnet) on {TARGET_IP}...")
print(f"    Port 2323 open: {check_port(TARGET_IP, 2323)}")

r = subprocess.run([ADB, "devices"], capture_output=True, text=True)
print("[*] ADB devices:\n", r.stdout)
