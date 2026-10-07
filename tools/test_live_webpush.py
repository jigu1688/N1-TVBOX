import subprocess
import time
import urllib.request
import json

def test_live():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    # 1. Install latest APK
    print('[*] Installing latest APK to N1...')
    subprocess.run([adb, '-s', dev, 'install', '-r', '-d', 'NextGen_隔空传装_v1.0.apk'])

    # 2. Launch MainActivity
    print('[*] Launching MainActivity...')
    subprocess.run([adb, '-s', dev, 'shell', 'am', 'start', '-n', 'com.nextgen.webpush/.MainActivity'])
    time.sleep(2.5)

    # 3. Capture screen showing focused button
    print('[*] Capturing screen...')
    subprocess.run([adb, '-s', dev, 'shell', 'screencap', '-p', '/sdcard/webpush_tv_focused.png'])
    subprocess.run([adb, '-s', dev, 'pull', '/sdcard/webpush_tv_focused.png', r'C:\Users\jigu\.gemini\antigravity-ide\brain\59392cea-4993-4618-813e-365af128b445\webpush_tv_focused.png'])

    # 4. Test Web Upload via HTTP multipart
    print('[*] Testing HTTP Multipart upload to N1...')
    url = 'http://192.168.31.114:8888/api/upload'
    boundary = '----WebKitFormBoundaryTest12345'
    body_parts = [
        f'--{boundary}',
        'Content-Disposition: form-data; name="file"; filename="test_upload.txt"',
        'Content-Type: text/plain',
        '',
        'Hello Phicomm N1 WebPush Test Successful!',
        f'--{boundary}--',
        ''
    ]
    body = '\r\n'.join(body_parts).encode('utf-8')

    req = urllib.request.Request(url, data=body, headers={
        'Content-Type': f'multipart/form-data; boundary={boundary}',
        'X-Auto-Install': '0'
    })

    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = response.read().decode('utf-8')
            print('[+] HTTP Upload Test Result:', res_data)
    except Exception as e:
        print('[-] HTTP Upload Test Error:', e)

    # 5. Test Status JSON API
    try:
        with urllib.request.urlopen('http://192.168.31.114:8888/api/status', timeout=5) as resp:
            status_json = json.loads(resp.read().decode('utf-8'))
            print('[+] Status API Files:', status_json.get('files'))
    except Exception as e:
        print('[-] Status API Error:', e)

if __name__ == '__main__':
    test_live()
