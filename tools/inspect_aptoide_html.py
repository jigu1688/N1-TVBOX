import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

req = urllib.request.Request('https://tv.aptoide.com/', headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    for line in html.splitlines():
        if '.apk' in line or 'download' in line:
            print(line.strip())
