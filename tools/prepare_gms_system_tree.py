import os, shutil

src_root = 'tools/gapps_components'
dst_tree = 'tools/gms_overlay'
if os.path.exists(dst_tree):
    shutil.rmtree(dst_tree)
os.makedirs(dst_tree, exist_ok=True)

# Map extracted packages to system overlay
# Structure inside each component is: <pkg_name>/<dpi or common or nodpi>/<system_subfolder>...
for comp in os.listdir(src_root):
    comp_dir = os.path.join(src_root, comp)
    if not os.path.isdir(comp_dir):
        continue
    
    # Check subfolders: prioritize 'nodpi', then '320', then 'common', then any
    subdirs = os.listdir(comp_dir)
    chosen_sub = None
    for pref in ['nodpi', 'common', '320', 'arm64']:
        if pref in subdirs:
            chosen_sub = pref
            break
    if not chosen_sub and subdirs:
        chosen_sub = subdirs[0]
    
    if not chosen_sub:
        continue
        
    actual_content = os.path.join(comp_dir, chosen_sub)
    for root, dirs, files in os.walk(actual_content):
        for f in files:
            src_file = os.path.join(root, f)
            rel = os.path.relpath(src_file, actual_content)
            dst_file = os.path.join(dst_tree, rel)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)

print('[+] Created GMS system overlay directory tree:')
total_size = 0
for root, dirs, files in os.walk(dst_tree):
    for f in files:
        p = os.path.join(root, f)
        total_size += os.path.getsize(p)
        rel = os.path.relpath(p, dst_tree)
        if f.endswith('.apk') or f.endswith('.jar') or f.endswith('.xml'):
            print(f'  - {rel} ({os.path.getsize(p)/1024/1024:.2f} MB)')

print(f'\n[+] Total GMS Overlay Size: {total_size / 1024 / 1024:.2f} MB')
