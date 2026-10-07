import zipfile

with zipfile.ZipFile("extracted_webpad/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk") as z:
    for name in z.namelist():
        if "META-INF" in name:
            print(name)
