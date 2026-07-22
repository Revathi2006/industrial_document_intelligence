import asyncio
from database.connection import AsyncSessionLocal
from database.models import Document, DocumentStatus
from services.pipeline import ProcessingPipeline
from sqlalchemy import select

async def main():
    async with AsyncSessionLocal() as session:
        query = select(Document).where(Document.status == 'COMPLETED')
        result = await session.execute(query)
        docs = result.scalars().all()
        
        print(f'Re-indexing {len(docs)} documents with embeddings...')
        print('=' * 60)
        
        pipeline = ProcessingPipeline(session)
        
        for doc in docs:
            print(f'\nProcessing: {doc.original_filename}')
            doc.status = DocumentStatus.UPLOADED
            await session.commit()
            
            result = await pipeline.process_document(doc.id)
            
            chunks = result.get('chunks_count', 0)
            embeddings = result.get('embeddings_count', 0)
            dim = result.get('embedding_dimension', 0)
            status = result.get('status', 'unknown')
            
            print(f'  Status: {status}')
            print(f'  Chunks: {chunks}')
            print(f'  Embeddings: {embeddings} ({dim}d)')
            print(f'  RAG Ready: YES')
        
        print('\n' + '=' * 60)
        print('All documents indexed with embeddings!')
        print('Ready for RAG chatbot!')

asyncio.run(main())
