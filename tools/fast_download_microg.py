import urllib.request
import ssl
import os
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0'}

downloads = [
    (
        "https://ghfast.top/https://github.com/microg/GmsCore/releases/download/v0.3.16.252432/com.google.android.gms-252432032.apk",
        "tools/microg_gmscore.apk",
        "microG GmsCore (Services Core)"
    ),
    (
        "https://ghfast.top/https://github.com/microg/GmsCore/releases/download/v0.3.16.252432/com.android.vending-84022632.apk",
        "tools/microg_fakestore.apk",
        "microG Companion (Play Store Stub / FakeStore)"
    ),
    (
        "https://ghfast.top/https://github.com/microg/GsfProxy/releases/download/v0.1.0/GsfProxy.apk",
        "tools/microg_gsfproxy.apk",
        "microG Services Framework Proxy"
    )
]

for url, dest, label in downloads:
    print(f"[*] Downloading {label}...")
    print(f"    Source: {url}")
    print(f"    Target: {dest}")
    
    if os.path.exists(dest) and os.path.getsize(dest) > 100000:
        print(f"    [SKIP] Already downloaded ({os.path.getsize(dest)/1024/1024:.2f} MB)")
        continue
        
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
            total_size = int(resp.headers.get('Content-Length', 0))
            downloaded = 0
            chunk_size = 65536
            with open(dest, 'wb') as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = downloaded / total_size * 100
                        sys.stdout.write(f"\r    [{downloaded/1024/1024:.1f}/{total_size/1024/1024:.1f} MB] ({pct:.1f}%)")
                        sys.stdout.flush()
            print(f"\n    [+] Successfully downloaded {dest} ({os.path.getsize(dest)/1024/1024:.2f} MB)")
    except Exception as e:
        print(f"\n    [!] Error downloading {dest}: {e}")
        if os.path.exists(dest):
            os.remove(dest)

print("\n[*] Checking downloaded components:")
for _, dest, label in downloads:
    if os.path.exists(dest):
        print(f"  [OK] {label}: {os.path.getsize(dest)/1024/1024:.2f} MB")
    else:
        print(f"  [MISSING] {label}: Not found!")
