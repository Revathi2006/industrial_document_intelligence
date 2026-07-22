from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from loguru import logger
from sklearn.metrics.pairwise import cosine_similarity
import pickle
from pathlib import Path
from config import settings

class EmbeddingGenerator:
    def __init__(self):
        self.model = None
        self.model_name = "all-MiniLM-L6-v2"
        self.dimension = 384
        self.embeddings_file = settings.EMBEDDINGS_DIR / "embeddings.pkl"
        self.embeddings_cache = {}
    
    def load_model(self):
        if self.model is None:
            logger.info(f"Loading model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info(f"Model loaded. Dimension: {self.dimension}")
        return self.model
    
    def generate_embeddings(self, chunks):
        model = self.load_model()
        texts = [chunk['text'] for chunk in chunks]
        logger.info(f"Generating embeddings for {len(texts)} chunks...")
        embeddings = model.encode(texts, normalize_embeddings=True)
        
        results = []
        for i, chunk in enumerate(chunks):
            results.append({
                'chunk_id': chunk.get('id', f'chunk_{i}'),
                'text': chunk['text'],
                'embedding': embeddings[i].tolist(),
                'dimension': self.dimension
            })
        
        logger.info(f"Generated {len(results)} embeddings")
        return results
    
    def store_embeddings(self, document_id, embeddings_data):
        self.embeddings_cache[document_id] = embeddings_data
        self._save_to_disk()
        logger.info(f"Stored {len(embeddings_data)} embeddings for doc {document_id}")
    
    def _save_to_disk(self):
        self.embeddings_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.embeddings_file, 'wb') as f:
            pickle.dump(self.embeddings_cache, f)
    
    def load_from_disk(self):
        if self.embeddings_file.exists():
            with open(self.embeddings_file, 'rb') as f:
                self.embeddings_cache = pickle.load(f)
            logger.info(f"Loaded embeddings for {len(self.embeddings_cache)} documents")
    
    def search_similar(self, query, top_k=5):
        model = self.load_model()
        query_embedding = model.encode([query], normalize_embeddings=True)[0]
        
        results = []
        for doc_id, chunks in self.embeddings_cache.items():
            for chunk in chunks:
                chunk_emb = np.array(chunk['embedding']).reshape(1, -1)
                query_emb = query_embedding.reshape(1, -1)
                similarity = cosine_similarity(chunk_emb, query_emb)[0][0]
                
                results.append({
                    'document_id': doc_id,
                    'chunk_id': chunk['chunk_id'],
                    'text': chunk['text'][:200],
                    'similarity_score': float(similarity)
                })
        
        results.sort(key=lambda x: x['similarity_score'], reverse=True)
        return results[:top_k]
    
    def get_stats(self):
        total_chunks = sum(len(c) for c in self.embeddings_cache.values())
        return {
            'total_documents_indexed': len(self.embeddings_cache),
            'total_chunks_embedded': total_chunks,
            'model': self.model_name,
            'dimension': self.dimension
        }

# Create the global instance
embedding_generator = EmbeddingGenerator()

# Load existing embeddings
try:
    embedding_generator.load_from_disk()
except Exception as e:
    logger.warning(f"No existing embeddings: {e}")
