import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    ('tv.aptoide.com', 'http://apkins.aptoide.com/aptoide-tv-5.1.2.apk'),
    ('direct apkins', 'http://apkins.aptoide.com/aptoide-tv.apk'),
    ('raw link', 'https://tv.aptoide.com/'),
    ('f-droid aptoide', 'https://f-droid.org/repo/cm.aptoidetv.pt_1.apk')
]

for label, u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6, context=ctx) as resp:
            sz = resp.headers.get('Content-Length', '0')
            print(f"[OK] {label} ({u}) -> size: {sz} bytes, status: {resp.status}")
    except Exception as e:
        print(f"[FAIL] {label} ({u}) -> {e}")
