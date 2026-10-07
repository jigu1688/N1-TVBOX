import subprocess
import xml.etree.ElementTree as ET

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

subprocess.run([adb, '-s', dev, 'shell', 'uiautomator', 'dump', '/data/local/tmp/ui.xml'])
res = subprocess.run([adb, '-s', dev, 'shell', 'cat', '/data/local/tmp/ui.xml'], capture_output=True, text=True, encoding='utf-8', errors='ignore')

try:
    root = ET.fromstring(res.stdout)
    print('=== Live Screen UI Text Elements ===')
    for node in root.iter('node'):
        text = node.get('text', '')
        cls = node.get('class', '')
        if text.strip():
            print(f'[{cls}] -> {text}')
except Exception as e:
    print('XML Parse error:', e)
