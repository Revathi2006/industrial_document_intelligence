import requests
import json

print('Uploading and processing test document...')
print('='*60)

with open('test_sop.txt', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/documents/upload',
        files={'files': ('test_sop.txt', f, 'text/plain')}
    )

result = response.json()
print(json.dumps(result, indent=2))

if result.get('documents'):
    for doc in result['documents']:
        doc_id = doc['id']
        filename = doc['filename']
        status = doc['status']
        pages = doc['pages']
        words = doc['words']
        chunks = doc['chunks']
        
        print(f'\nDocument #{doc_id}: {filename}')
        print(f'   Status: {status}')
        print(f'   Pages: {pages}')
        print(f'   Words: {words}')
        print(f'   Chunks: {chunks}')
        
        if doc.get('metadata'):
            meta_keys = list(doc['metadata'].keys())
            print(f'   Metadata keys: {meta_keys}')
        
        if doc.get('chunks_preview'):
            print('   First chunks:')
            for chunk in doc['chunks_preview']:
                cn = chunk['chunk_number']
                cp = chunk['preview']
                print(f'     Chunk {cn}: {cp}')
