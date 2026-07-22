import asyncio
from database.connection import AsyncSessionLocal
from database.models import Document, DocumentStatus
from services.pipeline import ProcessingPipeline
from sqlalchemy import select

async def reprocess_images():
    async with AsyncSessionLocal() as session:
        # Find failed image documents
        query = select(Document).where(
            Document.file_type.in_(['.png', '.jpg', '.jpeg']),
            Document.status == 'FAILED'
        )
        result = await session.execute(query)
        docs = result.scalars().all()
        
        if not docs:
            print('No failed image documents found')
            # Check for any image docs
            query2 = select(Document).where(
                Document.file_type.in_(['.png', '.jpg', '.jpeg'])
            )
            result2 = await session.execute(query2)
            all_image_docs = result2.scalars().all()
            print(f'Found {len(all_image_docs)} image documents total')
            docs = all_image_docs
        
        pipeline = ProcessingPipeline(session)
        
        for doc in docs:
            print(f'Re-processing: {doc.original_filename}')
            doc.status = DocumentStatus.UPLOADED
            await session.commit()
            
            result = await pipeline.process_document(doc.id)
            status = result.get('status', 'unknown')
            words = result.get('word_count', 0)
            chunks = result.get('chunks_count', 0)
            
            print(f'  Status: {status}')
            print(f'  Words: {words}')
            print(f'  Chunks: {chunks}')
            print()

asyncio.run(reprocess_images())
