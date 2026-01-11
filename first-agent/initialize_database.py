# 1_setup_database.py
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

def setup_database():
    """Create pgvector extension and documents table"""
    
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT", 5432))
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    
    # Enable pgvector extension
    try:
        cur.execute("CREATE EXTENSION IF NOT EXISTS vector")
        print("✓ pgvector extension enabled")
    except Exception as e:
        print(f"pgvector already exists: {e}")
    
    # Create documents table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS documents (
        id BIGSERIAL PRIMARY KEY,
        title TEXT,
        content TEXT,
        embedding vector(384),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    
    cur.execute(create_table_query)
    print("✓ Documents table created")
    
    # Create index for faster similarity search
    index_query = """
    CREATE INDEX IF NOT EXISTS documents_embedding_idx 
    ON documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
    """
    
    cur.execute(index_query)
    print("✓ Vector index created")
    
    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_database()
