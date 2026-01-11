"""RAG Pipeline core logic"""
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
import os


class RAGPipeline:
    """Minimal RAG pipeline for retrieval and generation"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize RAG pipeline with embedding model and database connection"""
        # Initialize embedding model (force CPU usage)
        self.embedding_model = SentenceTransformer(model_name, device='cpu')

        # Database connection
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 5432))
        )
        self.conn.autocommit = True

    def retrieve_similar_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find most similar documents to the query"""
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)

        # Convert to string format for pgvector
        embedding_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"

        # Similarity search in PostgreSQL
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        search_query = f"""
            SELECT id, title, content,
                   1 - (embedding <=> '{embedding_str}'::vector) as similarity
            FROM documents
            ORDER BY embedding <=> '{embedding_str}'::vector
            LIMIT {top_k}
        """

        cur.execute(search_query)
        results = cur.fetchall()
        cur.close()

        return results

    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()
