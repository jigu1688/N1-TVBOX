import subprocess
import os
import sqlite3

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.106:5555'

os.makedirs('logs/live_debug', exist_ok=True)
subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/', 'logs/live_debug/'])

db_file = 'logs/live_debug/databases/sections.db'
if os.path.exists(db_file):
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    print('Tables in DB:', c.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall())
    try:
        print('Sections in DB:', c.execute("SELECT [uuid], [type], [title], [position], [visible] FROM sections;").fetchall())
    except Exception as e:
        print('Error reading sections:', e)
    conn.close()
