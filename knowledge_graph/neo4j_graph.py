from neo4j import GraphDatabase
import sqlite3
import json

class Neo4jKnowledgeGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "neo4j+s://c15e70ce.databases.neo4j.io",
            auth=("neo4j", "Cp8wOSZJuvsSQAbEhnhBN68_m1XUz5WwCh6-em57TGA")  # ⚠️ REPLACE WITH YOUR PASSWORD
        )
    
    def import_from_sqlite(self):
        """Import all data from SQLite to Neo4j"""
        conn = sqlite3.connect('doc_processor.db')
        c = conn.cursor()
        
        c.execute("SELECT id, original_filename, file_type, doc_metadata, page_count, word_count, status FROM documents")
        docs = c.fetchall()
        
        c.execute("SELECT d.id, c.chunk_number, c.content, c.word_count FROM chunks c JOIN documents d ON c.document_id=d.id")
        chunks = c.fetchall()
        
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            
            for doc in docs:
                session.run("""
                    CREATE (d:Document {
                        id: $id, name: $name, type: $type,
                        pages: $pages, words: $words, status: $status
                    })
                """, id=doc[0], name=doc[1], type=doc[2], 
                    pages=doc[4] or 0, words=doc[5] or 0, status=doc[6] or '')
                
                metadata = json.loads(doc[3]) if doc[3] else {}
                for equip in metadata.get('equipment_mentioned', []):
                    session.run("""
                        MATCH (d:Document {id: $did})
                        MERGE (e:Equipment {name: $ename})
                        CREATE (d)-[:MENTIONS]->(e)
                    """, did=doc[0], ename=equip)
                
                session.run("""
                    MATCH (d:Document {id: $did})
                    MERGE (c:Category {name: $cat})
                    CREATE (d)-[:BELONGS_TO]->(c)
                """, did=doc[0], cat=doc[2])
            
            for chunk in chunks:
                session.run("""
                    MATCH (d:Document {id: $did})
                    CREATE (c:Chunk {number: $num, content: $content, words: $words})
                    CREATE (d)-[:HAS_CHUNK]->(c)
                """, did=chunk[0], num=chunk[1], content=chunk[2][:200] if chunk[2] else "", words=chunk[3] or 0)
        
        conn.close()
        print(f"✅ Neo4j: {len(docs)} docs, {len(chunks)} chunks imported")
    
    def search(self, query):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Document)
                WHERE d.name CONTAINS $q
                RETURN d.name as document, d.type as type, d.pages as pages, d.words as words
                LIMIT 10
            """, q=query)
            return [dict(r) for r in result]
    
    def get_graph(self):
        with self.driver.session() as session:
            result = session.run("""
                MATCH (d:Document)
                OPTIONAL MATCH (d)-[:MENTIONS]->(e:Equipment)
                OPTIONAL MATCH (d)-[:HAS_CHUNK]->(c:Chunk)
                RETURN d, e, c LIMIT 30
            """)
            nodes = {}
            edges = []
            for record in result:
                d = record['d']
                nodes[d['id']] = {'id': d['id'], 'name': d.get('name',''), 'type': d.get('type',''), 'label': 'Document'}
                if record['e']:
                    e = record['e']
                    nodes[e['name']] = {'id': e['name'], 'name': e['name'], 'label': 'Equipment'}
                    edges.append({'from': d['id'], 'to': e['name'], 'type': 'MENTIONS'})
                if record['c']:
                    c = record['c']
                    cid = f"chunk_{c['number']}"
                    nodes[cid] = {'id': cid, 'name': f"Chunk {c['number']}", 'label': 'Chunk'}
                    edges.append({'from': d['id'], 'to': cid, 'type': 'HAS_CHUNK'})
            return {'nodes': list(nodes.values()), 'edges': edges}
    
    def get_stats(self):
        with self.driver.session() as session:
            result = session.run("MATCH (d:Document) RETURN count(d) as docs")
            docs = result.single()['docs']
            result = session.run("MATCH (e:Equipment) RETURN count(e) as equip")
            equip = result.single()['equip']
            result = session.run("MATCH (c:Chunk) RETURN count(c) as chunks")
            chunks = result.single()['chunks']
            return {'documents': docs, 'equipment': equip, 'chunks': chunks}
    
    def close(self):
        self.driver.close()