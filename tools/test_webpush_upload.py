import urllib.request
import json

def test_webpush():
    url_status = 'http://192.168.31.114:8888/api/status'
    print('[*] Querying WebPush status...')
    with urllib.request.urlopen(url_status, timeout=3) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        print('[+] Status:', json.dumps(data, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    test_webpush()
