import sqlite3

conn = sqlite3.connect('logs/sections.db')
c = conn.cursor()
print('Tables in logs/sections.db:')
for row in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
    print(' ', row[0])

print('\nApplications table columns and rows:')
try:
    cols = [d[0] for d in c.execute("SELECT * FROM applications LIMIT 1").description]
    print(' Columns:', cols)
    for row in c.execute("SELECT * FROM applications"):
        print(' ', row)
except Exception as e:
    print(' Applications query error:', e)
