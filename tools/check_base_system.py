import subprocess

def inspect_img(img_path):
    print(f"=== INSPECTING {img_path} ===")
    res_lib = subprocess.run(f'wsl debugfs -R "ls -l /lib" {img_path}', shell=True, capture_output=True, text=True, errors='ignore')
    for line in res_lib.stdout.splitlines():
        if '.ko' in line:
            print("  ", line)

    print("\n--- /app and /priv-app in base ---")
    res_app = subprocess.run(f'wsl debugfs -R "ls -l /app" {img_path}', shell=True, capture_output=True, text=True, errors='ignore')
    for line in res_app.stdout.splitlines()[:25]:
        print("  /app:", line)

inspect_img('build_rom/system_clean_base.raw.img')
