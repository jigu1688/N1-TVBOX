import subprocess, os, shutil, zipfile

zip_path = 'tools/open_gapps-arm64-7.1-pico-20220215.zip'
extract_tmp = 'tools/gapps_raw'
if os.path.exists(extract_tmp):
    shutil.rmtree(extract_tmp)
os.makedirs(extract_tmp, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_tmp)

seven_zip = r'C:\Program Files\7-Zip\7z.exe'

# Test extracting gmscore-arm64.tar.lz
out_test = 'tools/gapps_test_out'
if os.path.exists(out_test):
    shutil.rmtree(out_test)
os.makedirs(out_test, exist_ok=True)

cmd1 = f'"{seven_zip}" e "{extract_tmp}/Core/gmscore-arm64.tar.lz" -so'
cmd2 = f'"{seven_zip}" x -si -ttar -o"{out_test}"'
p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
p2 = subprocess.Popen(cmd2, stdin=p1.stdout, stdout=subprocess.PIPE, shell=True)
p1.stdout.close()
out, err = p2.communicate()

print('7z extract output:\n', out.decode('utf-8', errors='ignore')[-300:])
print('Extracted files:')
for root, dirs, files in os.walk(out_test):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), out_test)
        print('  -', rel)
