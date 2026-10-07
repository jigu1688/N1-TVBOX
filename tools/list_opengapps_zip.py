import zipfile

zip_path = 'tools/open_gapps-arm64-7.1-pico-20220215.zip'
with zipfile.ZipFile(zip_path, 'r') as z:
    for info in z.infolist():
        print(f"{info.filename} ({info.file_size / 1024 / 1024:.2f} MB)")
