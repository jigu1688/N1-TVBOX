import os, zipfile, lzma, tarfile, io, shutil

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

zip_path = 'tools/open_gapps-arm64-7.1-pico-20220215.zip'
raw_dir = 'tools/gapps_raw'
out_dir = 'tools/gapps_components'
if os.path.exists(out_dir):
    shutil.rmtree(out_dir)
os.makedirs(out_dir, exist_ok=True)

# Exclude SetupWizard to keep fast boot
exclude_pkgs = ['setupwizard', 'googleonetimeinitializer']

print('[*] Extracting all OpenGApps packages...')
with zipfile.ZipFile(zip_path, 'r') as z:
    for name in z.namelist():
        if name.endswith('.tar.lz'):
            pkg_name = os.path.basename(name).replace('.tar.lz', '')
            if any(ex in pkg_name.lower() for ex in exclude_pkgs):
                print(f'  [-] Skipping {pkg_name} (Excluded for instant boot & TV stability)')
                continue
            
            raw_lz = z.read(name)
            try:
                tar_bytes = decompress_lzip(raw_lz)
                tar = tarfile.open(fileobj=io.BytesIO(tar_bytes))
                pkg_out = os.path.join(out_dir, pkg_name)
                tar.extractall(pkg_out)
                print(f'  [+] Extracted: {pkg_name} ({len(tar_bytes)/1024/1024:.2f} MB tar)')
            except Exception as e:
                print(f'  [!] Failed {pkg_name}: {e}')

print('[+] OpenGApps extraction successfully finished!')
