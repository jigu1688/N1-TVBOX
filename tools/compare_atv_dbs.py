import subprocess, time, os, sqlite3, sys
sys.stdout.reconfigure(encoding='utf-8')

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

# Start ATV fresh - it was already cleared
subprocess.run([adb, '-s', dev, 'shell', 
    'am start -n ca.dstudio.atvlauncher.pro/ca.dstudio.atvlauncher.screens.launcher.LauncherActivity'])
time.sleep(10)

# Check what files exist now
print('=== Files after 10s of ATV running ===')
r = subprocess.run([adb, '-s', dev, 'shell', 
    'ls -la /data/data/ca.dstudio.atvlauncher.pro/databases/'], 
    capture_output=True, text=True)
print(r.stdout)

# Root copy to tmp then pull
subprocess.run([adb, '-s', dev, 'shell', 
    'cp /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db /data/local/tmp/fresh_sections.db'],
    capture_output=True)
subprocess.run([adb, '-s', dev, 'shell', 
    'cp /data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal /data/local/tmp/fresh_sections.db-wal'],
    capture_output=True)

os.makedirs('logs/atv_fresh', exist_ok=True)
subprocess.run([adb, '-s', dev, 'pull', '/data/local/tmp/fresh_sections.db', 'logs/atv_fresh/sections.db'],
    capture_output=True)
subprocess.run([adb, '-s', dev, 'pull', '/data/local/tmp/fresh_sections.db-wal', 'logs/atv_fresh/sections.db-wal'],
    capture_output=True)

for f in ['sections.db', 'sections.db-wal']:
    p = os.path.join('logs', 'atv_fresh', f)
    if os.path.exists(p):
        print(f'{f}: {os.path.getsize(p)} bytes')
    else:
        print(f'{f}: NOT FOUND')

# Read the database WITH wal
conn = sqlite3.connect('logs/atv_fresh/sections.db')
c = conn.cursor()

print('\n--- Tables ---')
c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
for t in c.fetchall():
    tname = t[0]
    print(f'  {tname}')
    try:
        c.execute(f'SELECT count(*) FROM [{tname}]')
        cnt = c.fetchone()[0]
        print(f'    rows: {cnt}')
    except:
        pass

print('\n--- room_master_table ---')
try:
    c.execute('SELECT * FROM room_master_table')
    for row in c.fetchall():
        print(f'  FRESH: {row}')
except Exception as e:
    print(f'  Error: {e}')

print('\n--- Sections ---')
try:
    c.execute('SELECT * FROM sections')
    cols = [d[0] for d in c.description]
    print(f'  Columns: {cols}')
    for row in c.fetchall():
        print(f'  {row}')
except Exception as e:
    print(f'  Error: {e}')

print('\n--- Applications schema (PRAGMA) ---')
try:
    c.execute('PRAGMA table_info(applications)')
    for row in c.fetchall():
        print(f'  {row}')
except Exception as e:
    print(f'  Error: {e}')

print('\n--- Applications first 5 ---')
try:
    c.execute('SELECT * FROM applications LIMIT 5')
    cols = [d[0] for d in c.description]
    print(f'  Columns: {cols}')
    for row in c.fetchall():
        print(f'  {row}')
except Exception as e:
    print(f'  Error: {e}')

print('\n--- Settings ---')
try:
    c.execute('SELECT * FROM settings')
    cols = [d[0] for d in c.description]
    print(f'  Columns: {cols}')
    for row in c.fetchall():
        print(f'  {row}')
except Exception as e:
    print(f'  Error: {e}')

conn.close()

# PRESET comparison
print('\n\n=== PRESET Database ===')
pdb = 'build_rom/system_root/etc/atvlauncher/sections.db'
conn2 = sqlite3.connect(pdb)
c2 = conn2.cursor()

print('--- Tables ---')
c2.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
for t in c2.fetchall():
    tname = t[0]
    print(f'  {tname}')
    try:
        c2.execute(f'SELECT count(*) FROM [{tname}]')
        cnt = c2.fetchone()[0]
        print(f'    rows: {cnt}')
    except:
        pass

print('\n--- room_master_table ---')
c2.execute('SELECT * FROM room_master_table')
for row in c2.fetchall():
    print(f'  PRESET: {row}')

print('\n--- Applications schema (PRAGMA) ---')
c2.execute('PRAGMA table_info(applications)')
for row in c2.fetchall():
    print(f'  {row}')

print('\n--- Schema SQL diff ---')
# Get full CREATE TABLE statements
c2_schemas = {}
c2.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
for name, sql in c2.fetchall():
    c2_schemas[name] = sql

conn2.close()

# Compare
conn3 = sqlite3.connect('logs/atv_fresh/sections.db')
c3 = conn3.cursor()
c3_schemas = {}
c3.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
for name, sql in c3.fetchall():
    c3_schemas[name] = sql
conn3.close()

all_tables = sorted(set(list(c2_schemas.keys()) + list(c3_schemas.keys())))
for t in all_tables:
    s_preset = c2_schemas.get(t, 'MISSING')
    s_fresh = c3_schemas.get(t, 'MISSING')
    if s_preset != s_fresh:
        print(f'\n  TABLE [{t}] DIFFERS:')
        print(f'    PRESET: {s_preset}')
        print(f'    FRESH:  {s_fresh}')
    else:
        print(f'  TABLE [{t}]: MATCH')
