import os, shutil

src_root = 'tools/gapps_components'
overlay_root = 'tools/gms_system_clean'

if os.path.exists(overlay_root):
    shutil.rmtree(overlay_root)
os.makedirs(overlay_root, exist_ok=True)

# Walk and copy relevant files
# For gmscore, only pick 'nodpi' version
total_files = 0
total_bytes = 0

for root, dirs, files in os.walk(src_root):
    # Skip multi-dpi duplicates in gmscore (skip 320, 480, only keep nodpi)
    if 'gmscore-arm64' in root and ('\\320\\' in root or '\\480\\' in root or '/320/' in root or '/480/' in root):
        continue
    # Skip heavy GoogleTTS (60MB)
    if 'googletts-arm64' in root:
        continue
        
    for f in files:
        if f.endswith('.apk') or f.endswith('.jar') or f.endswith('.xml'):
            src_file = os.path.join(root, f)
            
            # Find system relative path: after 'nodpi/' or 'common/' or 'arm64/'
            parts = src_file.replace('\\', '/').split('/')
            target_parts = []
            for i, p in enumerate(parts):
                if p in ['nodpi', 'common', 'arm64']:
                    target_parts = parts[i+1:]
                    break
            
            if not target_parts:
                continue
                
            rel_target = '/'.join(target_parts)
            dst_file = os.path.join(overlay_root, rel_target.replace('/', os.sep))
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(src_file, dst_file)
            
            fsize = os.path.getsize(dst_file)
            total_files += 1
            total_bytes += fsize
            print(f'[+] Packaged: {rel_target} ({fsize/1024/1024:.2f} MB)')

print(f'\n[+] Clean GMS System Overlay Ready: {total_files} files, {total_bytes/1024/1024:.2f} MB total')
