import urllib.request
import ssl
import os
import sys

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

downloads = [
    # 1. Official SmartTube (Stable TV Release)
    (
        "https://ghfast.top/https://github.com/yuliskov/SmartTube/releases/download/latest/smarttube_stable.apk",
        "tools/SmartTube.apk",
        "SmartTube (YouTube for Android TV)"
    ),
    # 2. Official Aptoide TV
    (
        "https://aptoide.org/apks/aptoide-tv.apk",
        "tools/AptoideTV.apk",
        "Aptoide TV (Official Android TV App Store)"
    )
]

for url, dest, label in downloads:
    print(f"[*] Downloading {label}...")
    print(f"    Source: {url}")
    print(f"    Target: {dest}")
    
    if os.path.exists(dest) and os.path.getsize(dest) > 5000000:
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
        # Try fallback for Aptoide TV if aptoide.org fails
        if "Aptoide" in label:
            fallback_url = "https://files.aptoide.com/aptoide-tv-5.1.2.apk"
            print(f"    [*] Trying Aptoide fallback: {fallback_url}...")
            try:
                req = urllib.request.Request(fallback_url, headers=headers)
                with urllib.request.urlopen(req, timeout=60, context=ctx) as resp:
                    with open(dest, 'wb') as f:
                        f.write(resp.read())
                print(f"    [+] Fallback downloaded {dest} ({os.path.getsize(dest)/1024/1024:.2f} MB)")
            except Exception as e2:
                print(f"    [!] Fallback failed: {e2}")

print("\n[*] Verifying downloaded TV apps:")
for _, dest, label in downloads:
    if os.path.exists(dest) and os.path.getsize(dest) > 1000000:
        print(f"  [OK] {label}: {os.path.getsize(dest)/1024/1024:.2f} MB")
    else:
        print(f"  [FAIL] {label}: File missing or too small!")
