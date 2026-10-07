import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    ('Nightly', 'https://gitlab.com/AuroraOSS/AuroraStore/-/jobs/artifacts/master/raw/app/build/outputs/apk/nightly/app-nightly.apk?job=buildNightly'),
    ('Release 4.8.4', 'https://gitlab.com/AuroraOSS/AuroraStore/-/jobs/artifacts/4.8.4/raw/app/build/outputs/apk/release/app-release.apk?job=buildRelease'),
    ('Gitlab Package', 'https://gitlab.com/api/v4/projects/AuroraOSS%2FAuroraStore/packages/generic/AuroraStore/4.8.4/AuroraStore_4.8.4.apk')
]

for label, u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10, context=ctx) as resp:
            sz = int(resp.headers.get('Content-Length', 0))
            print(f"[OK] {label} -> {sz/1024/1024:.2f} MB, status: {resp.status}")
    except Exception as e:
        print(f"[FAIL] {label} -> {e}")
