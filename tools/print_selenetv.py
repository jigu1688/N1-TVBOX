import sqlite3

conn = sqlite3.connect('logs/check_reverted.db')
c = conn.cursor()
c.execute("SELECT * FROM applications WHERE [package-name] = 'org.moontechlab.selenetv'")
cols = [desc[0] for desc in c.description]
row = c.fetchone()
for col, val in zip(cols, row):
    print(f'{col}: {val}')
conn.close()
