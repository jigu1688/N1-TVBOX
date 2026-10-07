import zipfile, os, sqlite3

with zipfile.ZipFile('logs/atv_backup/backup.mid') as z:
    z.extractall('logs/atv_backup/extracted')
    for info in z.infolist():
        print(f'{info.filename}: {info.file_size} bytes')

print('\n=== Extracted databases/sections.db ===')
db_path = 'logs/atv_backup/extracted/databases/sections.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    for r in c.fetchall():
        print('Table:', r[0])
    
    print('\n--- room_master_table ---')
    c.execute('SELECT * FROM room_master_table')
    for r in c.fetchall():
        print(r)
        
    print('\n--- sections ---')
    c.execute('SELECT uuid, title, position, visible, rows, cols FROM sections')
    for r in c.fetchall():
        print(r)

    print('\n--- applications ---')
    c.execute('SELECT [package-name], [section-uuid], [position] FROM applications')
    for r in c.fetchall():
        print(r)
    conn.close()

print('\n=== Extracted shared_prefs ===')
sp_dir = 'logs/atv_backup/extracted/shared_prefs'
if os.path.exists(sp_dir):
    for f in os.listdir(sp_dir):
        print(f'File: {f}')
        with open(os.path.join(sp_dir, f), 'r', encoding='utf-8', errors='ignore') as fp:
            print(fp.read())
