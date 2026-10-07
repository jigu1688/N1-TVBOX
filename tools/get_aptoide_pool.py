import urllib.request
import ssl
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'http://pool.apk.aptoide.com/1/aptoide-tv-5.1.2.apk'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Build/NHG47L; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/119.0.0.0 Safari/537.36'
}

dest = 'tools/AptoideTV.apk'

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        print("Status:", resp.status)
        data = resp.read()
        with open(dest, 'wb') as f:
            f.write(data)
    print(f"[+] Downloaded {dest}: {os.path.getsize(dest)/1024/1024:.2f} MB")
except Exception as e:
    print("[!] Failed pool download:", e)
