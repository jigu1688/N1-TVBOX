import socket, concurrent.futures

def check(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.3)
    try:
        s.connect((ip, 5555))
        s.close()
        return ip
    except:
        return None

print("[*] Scanning 192.168.31.0/24 port 5555...")
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as ex:
    futures = [ex.submit(check, f"192.168.31.{i}") for i in range(1, 255)]
    for f in concurrent.futures.as_completed(futures):
        res = f.result()
        if res:
            print(f"[+] FOUND 5555 at {res}!")
