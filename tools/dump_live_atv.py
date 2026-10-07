import subprocess
import sqlite3
import os

adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
dev = '192.168.31.114:5555'

subprocess.run([adb, '-s', dev, 'shell', 'killall ca.dstudio.atvlauncher.pro'])
subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/sections_live.db'])
subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal', 'logs/sections_live.db-wal'])

conn = sqlite3.connect('logs/sections_live.db')
cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

for (tname,) in tables:
    print(f"\n=== TABLE: {tname} ===")
    cursor.execute(f"PRAGMA table_info({tname})")
    cols = [col[1] for col in cursor.fetchall()]
    print('Cols:', cols)
    cursor.execute(f"SELECT * FROM {tname}")
    for r in cursor.fetchall():
        print(dict(zip(cols, r)))
