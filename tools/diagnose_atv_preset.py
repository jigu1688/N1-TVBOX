import subprocess, sqlite3, sys, os, time
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# 1. Force stop ATV
subprocess.run([adb, '-s', dev, 'shell', 'am', 'force-stop', 'ca.dstudio.atvlauncher.pro'])
time.sleep(1)

# 2. Checkpoint WAL on device via adb shell
subprocess.run([adb, '-s', dev, 'shell', 
    'sqlite3 /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db "PRAGMA wal_checkpoint(TRUNCATE);"'])
time.sleep(0.5)

# 3. Pull checkpointed db
subprocess.run([adb, '-s', dev, 'pull', 
    '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/live_checkpointed.db'])

print(f'=== Live DB size: {os.path.getsize("logs/live_checkpointed.db")} bytes ===')

conn = sqlite3.connect('logs/live_checkpointed.db')
c = conn.cursor()

print('\n--- Tables ---')
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
for r in c.fetchall():
    print(r[0])

try:
    print('\n--- room_master_table ---')
    c.execute('SELECT * FROM room_master_table')
    for r in c.fetchall():
        print('LIVE room:', r)
except:
    print('No room_master_table in live db')

try:
    print('\n--- sections ---')
    c.execute('SELECT uuid, title, position, visible, rows, cols FROM sections')
    for r in c.fetchall():
        print(r)
except Exception as e:
    print('sections error:', e)

try:
    print('\n--- applications ---')
    c.execute('SELECT [package-name], [section-uuid], [position] FROM applications')
    for r in c.fetchall():
        print(r)
except Exception as e:
    print('applications error:', e)

try:
    print('\n--- settings wallpaper ---')
    c.execute("SELECT key, value FROM settings WHERE key LIKE '%wallpaper%'")
    for r in c.fetchall():
        print(r)
except Exception as e:
    print('settings error:', e)

conn.close()

# 4. Compare with preset db
print('\n\n=== PRESET DB ===')
preset_path = 'build_rom/system_root/etc/atvlauncher/sections.db'
print(f'Preset size: {os.path.getsize(preset_path)} bytes')
conn2 = sqlite3.connect(preset_path)
c2 = conn2.cursor()
c2.execute('SELECT * FROM room_master_table')
for r in c2.fetchall():
    print('PRESET room:', r)

c2.execute('SELECT uuid, title, position, visible, rows, cols FROM sections')
for r in c2.fetchall():
    print('PRESET section:', r)
conn2.close()

# 5. Check if webpadinit ran the preset injection
print('\n=== Preset flag check ===')
r = subprocess.run([adb, '-s', dev, 'shell', 'ls -la /data/system/users/0/.atv_preset*'], 
    capture_output=True, text=True)
print(r.stdout.strip() or 'NO PRESET FLAG FOUND')
print(r.stderr.strip())

# 6. Check webpadinit.sh content on device
print('\n=== webpadinit.sh on device (first boot section) ===')
r = subprocess.run([adb, '-s', dev, 'shell', 'grep -n "atv_preset\\|sections.db\\|disable\\|enable" /system/bin/webpadinit.sh'], 
    capture_output=True, text=True)
print(r.stdout)
