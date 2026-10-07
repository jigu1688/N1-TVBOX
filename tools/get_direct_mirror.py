import urllib.request, re

url = 'https://sourceforge.net/projects/opengapps/files/arm64/20220215/open_gapps-arm64-7.1-pico-20220215.zip/download'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    for line in html.splitlines():
        if 'http' in line and 'zip' in line:
            print(line.strip())
