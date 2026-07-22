from fastapi import APIRouter, Query
from knowledge_graph.graph_builder import KnowledgeGraph

router = APIRouter()
kg = KnowledgeGraph()

@router.get("/query")
async def query(q: str = Query(...)):
    return kg.query(q)

@router.get("/equipment")
async def equipment():
    return kg.get_all_equipment()

@router.get("/documents")
async def documents():
    return kg.get_documents()

@router.get("/document/{doc_id}/relationships")
async def doc_relationships(doc_id: int):
    return kg.get_relationships(doc_id)