from knowledge_graph.graph_builder import KnowledgeGraph
kg = KnowledgeGraph()
result = kg.query('image')
print('Image documents:', result)
print()
# Check document 3 relationships
rels = kg.get_relationships(3)
print('Document 3 relationships:', rels)
