import urllib.request, re, os, subprocess

initial_url = 'https://sourceforge.net/projects/opengapps/files/arm64/20220215/open_gapps-arm64-7.1-pico-20220215.zip/download'
req = urllib.request.Request(initial_url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

print('[*] Requesting SourceForge download token...')
with urllib.request.urlopen(req, timeout=15) as resp:
    html = resp.read().decode('utf-8', errors='ignore')
    match = re.search(r'content="5;\s*url=([^"]+)"', html)
    if not match:
        raise RuntimeError('Failed to find direct redirect URL')
    direct_url = match.group(1).replace('&amp;', '&')

print('[*] Direct Download URL:', direct_url)
zip_path = 'tools/open_gapps-arm64-7.1-pico.zip'

cmd = [
    'curl.exe', '-k', '-L',
    '-e', initial_url,
    '-A', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    '-o', zip_path,
    direct_url
]
print('[*] Running curl download...')
subprocess.run(cmd, check=True)

if os.path.exists(zip_path):
    print(f'[+] Downloaded size: {os.path.getsize(zip_path) / 1024 / 1024:.2f} MB')
