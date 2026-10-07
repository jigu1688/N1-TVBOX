import subprocess, re

for script in ['tools/build_v8_5_perfect.py', 'tools/build_v18_6_global.py']:
    print(f"\n=================== Checking {script} ===================")
    with open(script, 'r', encoding='utf-8') as f:
        content = f.read()

    writes = re.findall(r'"write\s+([^\s]+)\s+([^\s]+)"', content)
    results = []
    for src, dst in writes:
        cmd = ['wsl', 'debugfs', '-R', f'stat {dst}', '/mnt/d/github/N1盒子/extracted_aml/system.raw.img']
        res = subprocess.run(cmd, capture_output=True, text=True)
        exists = ('File not found' not in res.stdout) and ('Inode:' in res.stdout)
        has_rm = f'"rm {dst}"' in content
        results.append((dst, exists, has_rm))
        if exists and not has_rm:
            print(f"BUG! {dst} exists in stock but has NO rm before write!")
        elif not exists and has_rm:
            print(f"NOTE: {dst} does not exist in stock but has rm")

