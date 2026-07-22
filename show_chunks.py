import sqlite3
conn = sqlite3.connect('doc_processor.db')
c = conn.cursor()
c.execute("SELECT content FROM chunks WHERE content LIKE '%Equipment_ID%'")
rows = c.fetchall()
for r in rows:
    print(r[0])
    print('='*50)
print(f'Total chunks with equipment data: {len(rows)}')
conn.close()
