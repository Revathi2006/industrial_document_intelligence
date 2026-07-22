from knowledge_graph.graph_builder import KnowledgeGraph
kg = KnowledgeGraph()
print('Equipment found:')
for e in kg.get_all_equipment():
    eid = e['id']
    count = e['document_count']
    print(f'  {eid}: {count} documents')
print()
print('Motor related:')
print(kg.query('motor'))
