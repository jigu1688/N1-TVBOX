import urllib.request
import ssl
import gzip
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Host': 'aptoi.de'
}

dest = 'tools/AptoideTV.apk'

print("[*] Resolving http://aptoi.de/tv with proper Host header...")
try:
    req = urllib.request.Request('http://aptoi.de/tv', headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        print(f"[+] Final URL: {resp.geturl()}")
        data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
        print(f"[+] Downloaded {dest}: {os.path.getsize(dest)/1024/1024:.2f} MB")
except Exception as e:
    print("[!] Failed:", e)
