import sqlite3
conn = sqlite3.connect('doc_processor.db')
c = conn.cursor()
c.execute("SELECT content FROM chunks WHERE content LIKE '%BLR-201%'")
rows = c.fetchall()
print(f'Found {len(rows)} chunks with BLR-201')
for r in rows[:3]:
    print(r[0][:300])
    print('---')
conn.close()
