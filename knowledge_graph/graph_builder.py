import sqlite3
import json
from collections import defaultdict
import re

class KnowledgeGraph:
    def __init__(self):
        self.conn = sqlite3.connect('doc_processor.db')
        self.graph = defaultdict(list)
        self._build_graph()
    
    def _build_graph(self):
        c = self.conn.cursor()
        c.execute("SELECT id, original_filename, file_type, doc_metadata, page_count, word_count FROM documents")
        
        for row in c.fetchall():
            doc_id = row[0]
            filename = row[1]
            file_type = row[2]
            metadata = json.loads(row[3]) if row[3] else {}
            
            self.graph['documents'].append({
                'id': doc_id, 'name': filename, 'type': file_type,
                'pages': row[4], 'words': row[5]
            })
            
            for equip in metadata.get('equipment_mentioned', []):
                self.graph[f'equipment:{equip}'].append({'doc_id': doc_id, 'doc_name': filename})
            
            for cat in ['motor', 'pump', 'compressor', 'boiler', 'inspection', 'maintenance', 'manual']:
                if cat in filename.lower() or cat in str(metadata).lower():
                    self.graph[f'category:{cat}'].append({'doc_id': doc_id, 'doc_name': filename})
    
    def query(self, question):
        q = question.lower()
        equip_match = re.search(r'[A-Z]{2,4}-\d{3}', question.upper())
        if equip_match:
            eid = equip_match.group()
            related = self.graph.get(f'equipment:{eid}', [])
            return {'type': 'equipment', 'query': eid, 'related_documents': related, 'count': len(related)}
        
        for cat in ['motor', 'pump', 'compressor', 'boiler', 'inspection', 'maintenance']:
            if cat in q:
                related = self.graph.get(f'category:{cat}', [])
                return {'type': 'category', 'query': cat, 'related_documents': related, 'count': len(related)}
        
        return {'type': 'general', 'query': question, 'related_documents': [], 'count': 0}
    
    def get_all_equipment(self):
        equipment = []
        for key in self.graph:
            if key.startswith('equipment:'):
                eid = key.replace('equipment:', '')
                docs = self.graph[key]
                equipment.append({'id': eid, 'document_count': len(docs), 'documents': [d['doc_name'] for d in docs]})
        return equipment
    
    def get_relationships(self, doc_id):
        relationships = []
        for key, values in self.graph.items():
            for v in values:
                if v.get('doc_id') == doc_id:
                    relationships.append({'relation': key.split(':')[0], 'value': key.split(':')[1] if ':' in key else key})
        return relationships
    
    def get_documents(self):
        return self.graph.get('documents', [])