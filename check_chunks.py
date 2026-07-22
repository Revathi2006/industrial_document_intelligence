import sqlite3
conn = sqlite3.connect('doc_processor.db')
c = conn.cursor()
c.execute("SELECT c.content FROM chunks c JOIN documents d ON c.document_id=d.id WHERE d.file_type='.xlsx' OR d.file_type='.csv'")
rows = c.fetchall()
for i, r in enumerate(rows):
    print(f'CHUNK {i+1}:')
    print(r[0][:400])
    print('---')
print(f'Total chunks: {len(rows)}')
conn.close()
