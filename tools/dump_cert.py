import zipfile
import subprocess
import os

with zipfile.ZipFile("extracted_webpad/system_root/priv-app/PhiTvSettings/PhiTvSettings.apk") as z:
    z.extract("META-INF/CERT.RSA", "tools/re_tools")

subprocess.run(["keytool", "-printcert", "-file", "tools/re_tools/META-INF/CERT.RSA"])
