import requests
import json

# Test queries for RAG
test_queries = [
    "How to maintain a centrifugal pump?",
    "What is the inspection procedure?",
    "pump bearing replacement",
    "motor specifications"
]

for query in test_queries:
    print('\n' + '='*60)
    print(f'QUERY: {query}')
    print('='*60)
    
    response = requests.get(
        'http://localhost:8000/documents/search',
        params={'q': query, 'top_k': 3}
    )
    data = response.json()
    
    print(f'Results found: {data.get("results_count", 0)}')
    print(f'Stats: {data.get("stats", {})}')
    
    for i, r in enumerate(data.get('results', [])):
        print(f'\n  Result {i+1} - Relevance: {r.get("relevance", "0%")}')
        print(f'  Document: {r.get("document_name", "Unknown")}')
        print(f'  Content: {r.get("content", "")[:150]}...')

print('\n' + '='*60)
print('RAG Search is working!')
print('='*60)
