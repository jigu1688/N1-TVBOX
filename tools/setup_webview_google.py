import os, shutil

# Create /system/app/WebViewGoogle
dst_dir = 'build_rom/system_root/app/WebViewGoogle'
os.makedirs(dst_dir, exist_ok=True)
dst_apk = os.path.join(dst_dir, 'WebViewGoogle.apk')
shutil.copy2('tools/webview_119_arm64.apk', dst_apk)

# Clean old webview directory (old WebView 52)
old_webview = 'build_rom/system_root/app/webview'
if os.path.exists(old_webview):
    shutil.rmtree(old_webview, ignore_errors=True)

size_mb = os.path.getsize(dst_apk) / (1024 * 1024)
print(f'[+] Configured WebViewGoogle in {dst_dir}: {size_mb:.2f} MB')
