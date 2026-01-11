# 3_embeddings_storage.py
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import execute_values
import os
from dotenv import load_dotenv
from data_loader import SimpleDocumentLoader

load_dotenv()

class EmbeddingManager:
    """Generate and manage embeddings"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize embedding model (local, no API key needed)"""
        self.model = SentenceTransformer(model_name, device="cpu")
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"✓ Loaded model: {model_name} (dim: {self.embedding_dim})")
    
    def generate_embeddings(self, texts: list[str]) -> list:
        """Generate embeddings for multiple texts"""
        return self.model.encode(texts, convert_to_numpy=True, device="cpu")

class DatabaseManager:
    """Manage database operations"""
    
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 5432))
        )
    
    def store_embeddings(self, documents: list[dict], embeddings: list) -> int:
        """Store documents and their embeddings in PostgreSQL"""
        cur = self.conn.cursor()
        
        # Prepare data for insertion
        data = [
            (doc["title"], doc["content"], embedding.tolist())
            for doc, embedding in zip(documents, embeddings)
        ]
        
        insert_query = """
        INSERT INTO documents (title, content, embedding) 
        VALUES %s
        """
        
        execute_values(cur, insert_query, data)
        self.conn.commit()
        
        row_count = cur.rowcount
        cur.close()
        
        return row_count
    
    def close(self):
        self.conn.close()

# Main pipeline
if __name__ == "__main__":
    # 1. Load documents
    loader = SimpleDocumentLoader()
    documents = loader.load_from_list([
        {
            "title": "Climate Change Facts",
            "content": "Climate change refers to long-term shifts in temperatures and weather patterns..."
        },
        # Add more documents...
    ])
    print(f"✓ Loaded {len(documents)} documents")
    
    # 2. Generate embeddings
    embedding_mgr = EmbeddingManager()
    contents = [doc["content"] for doc in documents]
    embeddings = embedding_mgr.generate_embeddings(contents)
    print(f"✓ Generated {len(embeddings)} embeddings")
    
    # 3. Store in database
    db_mgr = DatabaseManager()
    stored = db_mgr.store_embeddings(documents, embeddings)
    print(f"✓ Stored {stored} documents in PostgreSQL")
    
    db_mgr.close()
