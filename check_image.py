import sqlite3
conn = sqlite3.connect('doc_processor.db')
c = conn.cursor()
c.execute("SELECT c.content FROM chunks c JOIN documents d ON c.document_id=d.id WHERE d.file_type='.jpeg' OR d.file_type='.png' OR d.file_type='.jpg'")
rows = c.fetchall()
for r in rows:
    print('Image content:')
    print(r[0])
    print('---')
conn.close()
