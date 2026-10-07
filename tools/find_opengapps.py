import urllib.request, json

req = urllib.request.Request('https://api.github.com/repos/opengapps/arm64/releases', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=10) as response:
    data = json.loads(response.read().decode())
    for r in data:
        for a in r.get('assets', []):
            name = a.get('name', '')
            if '7.1' in name and any(k in name for k in ['pico', 'tvstock', 'nano']):
                size_mb = a.get('size', 0) / 1024 / 1024
                print(f"{name} ({size_mb:.2f} MB) -> {a.get('browser_download_url')}")
