import zipfile, io, tarfile, lzma, os, subprocess

zip_path = 'tools/open_gapps-arm64-7.1-pico-20220215.zip'
apksigner = r'C:\Users\jigu\AppData\Local\Android\Sdk\build-tools\36.0.0\apksigner.bat'

def calc_dict_size(code):
    base = 1 << (code & 0x1F)
    fraction = (code >> 5) & 0x07
    return base - (fraction * (base // 16))

def decompress_lzip(data):
    code = data[5]
    dsize = calc_dict_size(code)
    payload = data[6:-20]
    filters = [{
        'id': lzma.FILTER_LZMA1,
        'dict_size': dsize,
        'lc': 3,
        'lp': 0,
        'pb': 2
    }]
    decomp = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=filters)
    return decomp.decompress(payload)

tmp_dir = 'tools/orig_gapps_test'
os.makedirs(tmp_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    for name in z.namelist():
        if name.endswith('.tar.lz'):
            raw = z.read(name)
            tar_data = decompress_lzip(raw)
            tar = tarfile.open(fileobj=io.BytesIO(tar_data))
            for member in tar.getmembers():
                if member.name.endswith('.apk'):
                    apk_bytes = tar.extractfile(member).read()
                    out_name = os.path.basename(member.name)
                    out_p = os.path.join(tmp_dir, out_name)
                    with open(out_p, 'wb') as f:
                        f.write(apk_bytes)
                    print(f"Extracted {out_name} ({len(apk_bytes)/1024/1024:.2f} MB)")
                    
                    # Verify certificate
                    res = subprocess.run(f'{apksigner} verify --print-certs "{out_p}"', shell=True, capture_output=True, text=True, errors='ignore')
                    print(f"--- Cert for {out_name} ---")
                    for line in res.stdout.splitlines():
                        if any(k in line for k in ['Signer', 'Subject', 'SHA-256']):
                            print('  ', line)
                    if res.returncode != 0:
                        print("  [!] verify returncode:", res.returncode, res.stderr)
