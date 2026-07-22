import sqlite3
import json
import os

# Connect to database
db_path = 'doc_processor.db'

if not os.path.exists(db_path):
    print("❌ Database file not found!")
    exit()

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=" * 70)
print("🗄️  DATABASE EXPLORER")
print("=" * 70)

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("\n📊 Tables in database:")
for table in tables:
    print(f"  📁 {table[0]}")

# Count records in each table
print("\n📈 Record Counts:")
for table in tables:
    try:
        cursor.execute(f"SELECT COUNT(*) FROM {table[0]};")
        count = cursor.fetchone()[0]
        print(f"  {table[0]}: {count} records")
    except:
        pass

# Show documents
print("\n" + "=" * 70)
print("📄 DOCUMENTS")
print("=" * 70)
cursor.execute("SELECT id, original_filename, file_type, status, file_size, page_count, word_count, language FROM documents;")
docs = cursor.fetchall()
for doc in docs:
    print(f"\n  ID: {doc[0]}")
    print(f"  Filename: {doc[1]}")
    print(f"  Type: {doc[2]}")
    print(f"  Status: {doc[3]}")
    print(f"  Size: {doc[4]} bytes ({doc[4]/1024:.1f} KB)" if doc[4] else "  Size: N/A")
    print(f"  Pages: {doc[5] or 0}")
    print(f"  Words: {doc[6] or 0}")
    print(f"  Language: {doc[7] or 'N/A'}")

# Show chunks
print("\n" + "=" * 70)
print("✂️  CHUNKS")
print("=" * 70)
cursor.execute("SELECT id, document_id, chunk_number, word_count, section, substr(content, 1, 100) FROM chunks;")
chunks = cursor.fetchall()
if chunks:
    for chunk in chunks:
        print(f"\n  Chunk ID: {chunk[0]}")
        print(f"  Document ID: {chunk[1]}")
        print(f"  Chunk #: {chunk[2]}")
        print(f"  Words: {chunk[3]}")
        print(f"  Section: {chunk[4]}")
        print(f"  Preview: {chunk[5]}...")
else:
    print("  ❌ No chunks found! Document needs processing.")
    print("  Run: python -c \"import asyncio; from database.connection import AsyncSessionLocal; from services.pipeline import ProcessingPipeline; async def p(): async with AsyncSessionLocal() as s: await ProcessingPipeline(s).process_document(1); asyncio.run(p())\"")

# Show metadata
print("\n" + "=" * 70)
print("🏷️  METADATA")
print("=" * 70)
cursor.execute("SELECT id, original_filename, doc_metadata FROM documents WHERE doc_metadata IS NOT NULL;")
meta = cursor.fetchall()
if meta:
    for m in meta:
        print(f"\n  Document ID: {m[0]} - {m[1]}")
        if m[2]:
            metadata = json.loads(m[2]) if isinstance(m[2], str) else m[2]
            for key, value in metadata.items():
                print(f"    {key}: {value}")
else:
    print("  No metadata extracted yet")

# Show audit logs
print("\n" + "=" * 70)
print("📋 RECENT AUDIT LOGS")
print("=" * 70)
try:
    cursor.execute("SELECT document_id, action, created_at FROM audit_logs ORDER BY created_at DESC LIMIT 10;")
    logs = cursor.fetchall()
    for log in logs:
        print(f"  Doc {log[0]}: {log[1]} at {log[2]}")
except:
    print("  No audit logs")

conn.close()
print("\n" + "=" * 70)
print("✅ Database exploration complete!")
print("=" * 70)
