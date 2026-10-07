import urllib.request
import json
import os

headers = {'User-Agent': 'Mozilla/5.0'}

def get_release(repo):
    url = f'https://api.github.com/repos/{repo}/releases/latest'
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("[*] 1. Checking microG GmsCore releases...")
try:
    rel = get_release('microg/GmsCore')
    print(f"  Tag: {rel.get('tag_name')}")
    for a in rel.get('assets', []):
        print(f"  Asset: {a.get('name')} -> {a.get('browser_download_url')}")
except Exception as e:
    print("  GmsCore error:", e)

print("\n[*] 2. Checking microG GsfProxy releases...")
try:
    rel = get_release('microg/GsfProxy')
    print(f"  Tag: {rel.get('tag_name')}")
    for a in rel.get('assets', []):
        print(f"  Asset: {a.get('name')} -> {a.get('browser_download_url')}")
except Exception as e:
    print("  GsfProxy error:", e)

print("\n[*] 3. Checking FakeStore releases...")
try:
    rel = get_release('microg/FakeStore')
    print(f"  Tag: {rel.get('tag_name')}")
    for a in rel.get('assets', []):
        print(f"  Asset: {a.get('name')} -> {a.get('browser_download_url')}")
except Exception as e:
    print("  FakeStore error:", e)
