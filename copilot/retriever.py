from services.embeddings import embedding_generator
import re
import sqlite3

class Retriever:
    def __init__(self):
        embedding_generator.load_from_disk()
        self._load_doc_info()
    
    def _load_doc_info(self):
        """Load document names from database"""
        self.doc_info = {}
        try:
            conn = sqlite3.connect('doc_processor.db')
            c = conn.cursor()
            c.execute("SELECT id, original_filename, page_count FROM documents")
            for row in c.fetchall():
                self.doc_info[row[0]] = {
                    'name': row[1],
                    'pages': row[2] or 1
                }
            conn.close()
        except:
            self.doc_info = {}
    
    def search(self, query, top_k=3):
        equip_match = re.search(r'[A-Z]{2,4}-\d{3}', query.upper())
        
        if equip_match:
            equip_id = equip_match.group()
            enhanced_query = f"{equip_id} equipment data specifications"
            results = embedding_generator.search_similar(enhanced_query, top_k=top_k)
        else:
            results = embedding_generator.search_similar(query, top_k=top_k)
        
        # Add document info to results
        enriched_results = []
        for r in results:
            doc_id = r['document_id']
            doc_info = self.doc_info.get(doc_id, {})
            
            # Estimate page number from chunk
            text = r['text']
            page_hint = ""
            if 'Page' in text:
                page_match = re.search(r'Page (\d+)', text)
                if page_match:
                    page_hint = f", Page {page_match.group(1)}"
            
            enriched_results.append({
                'text': r['text'],
                'doc_id': doc_id,
                'doc_name': doc_info.get('name', f'Doc #{doc_id}'),
                'total_pages': doc_info.get('pages', 1),
                'page_hint': page_hint,
                'score': round(r['similarity_score'] * 100, 1)
            })
        
        return enriched_results
    
    def get_context(self, query, top_k=3):
        results = self.search(query, top_k)
        if not results:
            results = self.search(query, top_k=8)
        
        context = '\n\n'.join([r['text'] for r in results])
        
        # Format sources with document name and pages
        sources = []
        for r in results:
            doc_name = r['doc_name']
            pages = r['total_pages']
            score = r['score']
            page_hint = r['page_hint']
            sources.append(f"{doc_name} ({pages} pages{page_hint}) - {score}% match")
        
        return context, sources