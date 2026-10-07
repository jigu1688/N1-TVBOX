import urllib.request

payload = '{"fileName":"SeleneTV-v1.4.6-arm64-v8a.apk"}'.encode('utf-8')
req = urllib.request.Request(
    'http://192.168.31.115:8888/api/install',
    data=payload,
    headers={'Content-Type': 'application/json'}
)
resp = urllib.request.urlopen(req, timeout=15)
print('Response:', resp.read().decode('utf-8'))
