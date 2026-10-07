import urllib.request, json

url = 'https://api.github.com/repos/uazo/cromite/releases/tags/v119.0.6045.200-91419aa0e8f321e4ff5cdceebaad8852323c2c86'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read().decode())
        print('Release:', data.get('tag_name'))
        for asset in data.get('assets', []):
            print(f"{asset['name']}: {asset['size'] / (1024*1024):.2f} MB -> {asset['browser_download_url']}")
except Exception as e:
    print('Error:', e)
