import sqlite3
conn = sqlite3.connect('doc_processor.db')
c = conn.cursor()
c.execute("SELECT c.content FROM chunks c JOIN documents d ON c.document_id=d.id WHERE d.file_type IN ('.jpeg','.jpg','.png')")
rows = c.fetchall()
for r in rows:
    print('IMAGE TEXT EXTRACTED:')
    print(r[0])
conn.close()
