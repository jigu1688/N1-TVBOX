import urllib.request
import ssl
import re
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

dest = 'tools/AptoideTV.apk'

print("[*] Fetching Uptodown download page...")
try:
    req = urllib.request.Request('https://cm-aptoidetv-pt.en.uptodown.com/android/download', headers=headers)
    with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        
    m = re.search(r'data-url=["\']([^"\']+)["\']', html)
    if m:
        dl_url = m.group(1)
        if dl_url.startswith('/'):
            dl_url = 'https://dw.uptodown.net' + dl_url
        print(f"[+] Found direct download URL: {dl_url}")
        
        # Download APK
        req_dl = urllib.request.Request(dl_url, headers=headers)
        with urllib.request.urlopen(req_dl, timeout=30, context=ctx) as resp_dl:
            with open(dest, 'wb') as f:
                f.write(resp_dl.read())
        print(f"[+] Downloaded AptoideTV.apk: {os.path.getsize(dest)/1024/1024:.2f} MB")
    else:
        print("[!] Could not parse download button URL from Uptodown")
except Exception as e:
    print("[!] Uptodown error:", e)
