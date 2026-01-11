# 4_rag_pipeline_mvp.py
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

class RAGPipelineMVP:
    """Minimal RAG pipeline"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        # Initialize components (force CPU usage due to CUDA compatibility)
        self.embedding_model = SentenceTransformer(model_name, device='cpu')

        # Initialize Google GenAI client
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

        # Database connection
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
            port=int(os.getenv("DB_PORT", 5432))
        )
        # Set autocommit for consistent query behavior
        self.conn.autocommit = True
    
    def retrieve_similar_documents(self, query: str, top_k: int = 3) -> list[dict]:
        """Find most similar documents to the query"""

        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)

        # Convert to string format for pgvector
        embedding_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"

        # Debug output
        print(f"  [DEBUG] Embedding string length: {len(embedding_str)}")

        # Similarity search in PostgreSQL
        # Note: Using f-string for embedding because %s::vector doesn't work with psycopg2
        cur = self.conn.cursor(cursor_factory=RealDictCursor)

        # First, verify we can see the documents at all
        cur.execute("SELECT COUNT(*) as count FROM documents")
        count_result = cur.fetchone()
        print(f"  [DEBUG] Document count in this transaction: {count_result['count']}")

        # Try the one-line format that worked in standalone test
        search_query = f"SELECT id, title, content, 1 - (embedding <=> '{embedding_str}'::vector) as similarity FROM documents ORDER BY embedding <=> '{embedding_str}'::vector LIMIT {top_k}"

        print(f"  [DEBUG] Executing one-line query...")
        cur.execute(search_query)
        results = cur.fetchall()
        print(f"  [DEBUG] Query returned {len(results)} results")
        cur.close()

        return results
    
    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using Google GenAI based on context"""

        prompt = f"""Based on the following context, answer the question.
If the context doesn't contain relevant information, say so.

Context:
{context}

Question: {query}

Answer:"""

        response = self.client.models.generate_content(
            model='gemini-2.5-flash-lite',
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=300,
            )
        )

        return response.text
    
    def query(self, question: str) -> dict:
        """Complete RAG pipeline: retrieve + generate"""
        
        # Step 1: Retrieve
        print(f"\n📝 Question: {question}")
        retrieved_docs = self.retrieve_similar_documents(question, top_k=3)
        
        print(f"✓ Retrieved {len(retrieved_docs)} documents")
        for i, doc in enumerate(retrieved_docs, 1):
            print(f"  {i}. {doc['title']} (similarity: {doc['similarity']:.3f})")
        
        # Step 2: Build context
        context = "\n\n".join([
            f"Document: {doc['title']}\n{doc['content']}"
            for doc in retrieved_docs
        ])
        
        # Step 3: Generate
        print("🤖 Generating answer...")
        answer = self.generate_answer(question, context)
        
        return {
            "question": question,
            "retrieved_documents": [
                {"title": doc["title"], "similarity": doc["similarity"]}
                for doc in retrieved_docs
            ],
            "answer": answer
        }
    
    def close(self):
        self.conn.close()

# Example usage
if __name__ == "__main__":
    rag = RAGPipelineMVP()
    
    # Test queries
    queries = [
        "What are the main causes of climate change?",
        "How does renewable energy work?",
        "What is machine learning?"
    ]
    
    for query in queries:
        result = rag.query(query)
        print(f"\n{'='*60}")
        print(f"Answer: {result['answer']}")
    
    rag.close()
