import urllib.request
import ssl
import re
import os

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
opener = urllib.request.build_opener(urllib.request.HTTPSHandler(context=ctx))

url = 'https://mirrors.kodi.tv/addons/matrix/resource.language.zh_cn/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with opener.open(req) as resp:
        html = resp.read().decode('utf-8')
        zips = re.findall(r'href=[\"\'](resource\.language\.zh_cn-[0-9\.]+\.zip)[\"\']', html)
        print('Available Chinese language zip files:', zips)
        if zips:
            latest_zip = zips[-1]
            zip_url = url + latest_zip
            print('Downloading latest:', zip_url)
            with opener.open(urllib.request.Request(zip_url, headers={'User-Agent': 'Mozilla/5.0'})) as zresp:
                with open('tools/' + latest_zip, 'wb') as f:
                    f.write(zresp.read())
            print('Downloaded to tools/' + latest_zip)
            # Copy to fixed name
            with open('tools/' + latest_zip, 'rb') as src, open('tools/resource.language.zh_cn.zip', 'wb') as dst:
                dst.write(src.read())
            print('Saved as tools/resource.language.zh_cn.zip')
except Exception as e:
    print('Error:', e)
