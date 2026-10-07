import urllib.request
import os

headers = {'User-Agent': 'Mozilla/5.0'}

downloads = [
    # microG GmsCore (标准版，包名 com.google.android.gms)
    ("https://github.com/microg/GmsCore/releases/download/v0.3.16.252432/com.google.android.gms-252432032.apk", "tools/microg_gmscore.apk"),
    # microG Companion (FakeStore，包名 com.android.vending，充当 Store 占位符)
    ("https://github.com/microg/GmsCore/releases/download/v0.3.16.252432/com.android.vending-84022632.apk", "tools/microg_fakestore.apk"),
    # GsfProxy (Google 框架代理)
    ("https://github.com/microg/GsfProxy/releases/download/v0.1.0/GsfProxy.apk", "tools/microg_gsfproxy.apk")
]

for url, dest in downloads:
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"[SKIP] {dest} already exists ({os.path.getsize(dest)/1024/1024:.2f} MB)")
        continue
    print(f"[*] Downloading {url} -> {dest}...")
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
            with open(dest, 'wb') as f:
                f.write(data)
        print(f"[+] Downloaded {dest} ({len(data)/1024/1024:.2f} MB)")
    except Exception as e:
        print(f"[!] Failed to download {dest}: {e}")
