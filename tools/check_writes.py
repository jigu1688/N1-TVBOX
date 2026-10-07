import re, subprocess

text = open('tools/build_v8_5_perfect.py', encoding='utf-8').read()
writes = re.findall(r'write\s+(\S+)\s+([^\s\"]+)', text)
for src, dst in writes:
    r = subprocess.run(['wsl', 'debugfs', '-R', f'stat {dst}', 'extracted_aml/system.raw.img'], capture_output=True, text=True)
    if 'Inode:' in r.stdout:
        print(f"EXISTS: {dst}")
    else:
        print(f"NEW   : {dst}")
