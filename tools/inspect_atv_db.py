import subprocess
import sqlite3

def inspect_sections():
    adb = r'C:\Users\jigu\AppData\Local\Android\Sdk\platform-tools\adb.exe'
    dev = '192.168.31.114:5555'

    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db', 'logs/sections.db'])
    subprocess.run([adb, '-s', dev, 'pull', '/data/data/ca.dstudio.atvlauncher.pro/databases/sections.db-wal', 'logs/sections.db-wal'])

    conn = sqlite3.connect('logs/sections.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    print('Tables in sections.db:', tables)

    for (tname,) in tables:
        print(f"\n=== TABLE: {tname} ===")
        cursor.execute(f"PRAGMA table_info({tname})")
        cols = [col[1] for col in cursor.fetchall()]
        print('Cols:', cols)
        cursor.execute(f"SELECT * FROM {tname}")
        for r in cursor.fetchall():
            print(dict(zip(cols, r)))

if __name__ == '__main__':
    inspect_sections()
