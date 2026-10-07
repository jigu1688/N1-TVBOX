import urllib.request, json

url = 'https://api.github.com/repos/uazo/cromite/releases?per_page=30'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        releases = json.loads(resp.read().decode())
        for rel in releases:
            tag = rel.get('tag_name', '')
            for asset in rel.get('assets', []):
                name = asset['name']
                if 'webview' in name.lower() and 'arm64' in name.lower():
                    print(f"Tag: {tag} -> {name}: {asset['size'] / (1024*1024):.2f} MB -> {asset['browser_download_url']}")
except Exception as e:
    print('Error:', e)
