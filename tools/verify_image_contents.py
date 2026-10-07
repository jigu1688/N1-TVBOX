import subprocess

res = subprocess.run(['wsl', 'debugfs', '-R', 'ls -l /app', 'build_rom/system.raw.img'], capture_output=True, text=True)
print("/app directory listing in build_rom/system.raw.img:")
for line in res.stdout.splitlines():
    if any(k in line for k in ['SmartTube', 'FDroid', 'WebPush', 'ATVLauncher', 'FileBrowser', 'NextGenWidget']):
        print(" ", line)

res_priv = subprocess.run(['wsl', 'debugfs', '-R', 'ls -l /priv-app', 'build_rom/system.raw.img'], capture_output=True, text=True)
print("\n/priv-app directory listing:")
for line in res_priv.stdout.splitlines():
    if any(k in line for k in ['GmsCore', 'FakeStore', 'GsfProxy', 'PhiCloudBox', 'PhiLauncher', 'PhiTvSettings']):
        print(" ", line)
