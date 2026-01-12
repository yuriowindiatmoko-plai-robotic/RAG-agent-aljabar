# fixed_rag_pipeline.py
"""
FIXED RAG Pipeline with Data Loading
- Proper database setup
- Document loading
- Working retrieval
- Google Gemini integration
"""

import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import RealDictCursor
import google.generativeai as genai
import json

load_dotenv()


class FixedRAGPipeline:
    """Complete RAG pipeline with data loading"""
    
    def __init__(self, embedding_model: str = "all-MiniLM-L6-v2"):
        """Initialize RAG components"""
        
        print("🚀 Initializing RAG Pipeline...")
        
        # 1. Initialize embedding model (384 dimensions for all-MiniLM-L6-v2)
        print("  ✓ Loading embedding model...")
        self.embedding_model = SentenceTransformer(embedding_model, device='cpu')
        self.embedding_dim = self.embedding_model.get_sentence_embedding_dimension()
        print(f"    Embedding dimension: {self.embedding_dim}")
        
        # 2. Initialize Gemini
        print("  ✓ Configuring Gemini API...")
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY or GEMINI_API_KEY not set in .env")
        genai.configure(api_key=api_key)
        print(f"    Using model: gemini-2.5-flash-lite")
        
        # 3. Connect to PostgreSQL
        print("  ✓ Connecting to PostgreSQL...")
        try:
            self.conn = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", ""),
                database=os.getenv("DB_NAME", "boilerplate_db"),
                port=int(os.getenv("DB_PORT", 5432))
            )
            print("    Connected successfully")
        except Exception as e:
            print(f"    ❌ Connection failed: {e}")
            raise
        
        # 4. Setup database
        print("  ✓ Setting up database...")
        self._setup_database()
        print("✅ RAG Pipeline initialized!\n")
    
    def _setup_database(self):
        """Create necessary tables and extensions"""
        cur = self.conn.cursor()

        try:
            # Install pgvector
            print("    Installing pgvector extension...")
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"    ⚠️ pgvector already installed: {e}")
            self.conn.rollback()

        try:
            # Check if table exists
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_name = 'documents'
                );
            """)
            table_exists = cur.fetchone()[0]

            if table_exists:
                print("    Table exists, checking schema...")
                # Check if UNIQUE constraint exists on title
                cur.execute("""
                    SELECT EXISTS (
                        SELECT 1
                        FROM pg_constraint
                        WHERE conrelid = 'documents'::regclass
                        AND contype = 'u'
                        AND conname = 'documents_title_key'
                    );
                """)
                has_unique = cur.fetchone()[0]

                if not has_unique:
                    print("    Adding UNIQUE constraint to title column...")
                    # First, remove duplicates if any
                    cur.execute("""
                        DELETE FROM documents d1
                        USING documents d2
                        WHERE d1.id > d2.id
                        AND d1.title = d2.title;
                    """)
                    # Add unique constraint
                    cur.execute("""
                        ALTER TABLE documents
                        ADD CONSTRAINT documents_title_key UNIQUE (title);
                    """)
                    print("    ✓ UNIQUE constraint added")
            else:
                # Create new documents table
                print("    Creating documents table...")
                cur.execute(f"""
                    CREATE TABLE documents (
                        id SERIAL PRIMARY KEY,
                        title TEXT NOT NULL UNIQUE,
                        content TEXT NOT NULL,
                        embedding vector({self.embedding_dim}),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)

            # Create index
            cur.execute("""
                CREATE INDEX IF NOT EXISTS idx_embedding
                ON documents USING ivfflat (embedding vector_cosine_ops);
            """)

            self.conn.commit()
            print("    Table created/verified")
        except psycopg2.Error as e:
            print(f"    ❌ Error creating table: {e}")
            self.conn.rollback()
            raise

        cur.close()
    
    def load_documents(self, documents: list[dict]) -> int:
        """Load documents with embeddings into database
        
        Args:
            documents: List of dicts with 'title' and 'content' keys
        
        Returns:
            Number of documents loaded
        """
        print(f"\n📥 Loading {len(documents)} documents...")
        
        cur = self.conn.cursor()
        loaded_count = 0
        
        for i, doc in enumerate(documents, 1):
            try:
                title = doc['title']
                content = doc['content']
                
                # Generate embedding
                embedding = self.embedding_model.encode(content)
                embedding_list = embedding.tolist()
                
                # Convert to pgvector format
                embedding_str = "[" + ",".join([str(x) for x in embedding_list]) + "]"
                
                # Insert into database
                cur.execute("""
                    INSERT INTO documents (title, content, embedding)
                    VALUES (%s, %s, %s::vector)
                    ON CONFLICT (title) DO NOTHING;
                """, (title, content, embedding_str))
                
                loaded_count += 1
                
                if i % 5 == 0:
                    print(f"  ✓ Loaded {i}/{len(documents)} documents...")
            
            except Exception as e:
                print(f"  ❌ Error loading '{doc.get('title', 'Unknown')}': {e}")
                continue
        
        self.conn.commit()
        cur.close()
        
        print(f"✅ Successfully loaded {loaded_count}/{len(documents)} documents\n")
        return loaded_count
    
    def retrieve_documents(self, query: str, top_k: int = 3) -> list[dict]:
        """Find most similar documents to query"""
        
        # Generate query embedding
        query_embedding = self.embedding_model.encode(query)
        embedding_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"
        
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Use proper pgvector syntax with parameterized query
        cur.execute(f"""
            SELECT
                id,
                title,
                content,
                1 - (embedding <=> %s::vector) as similarity
            FROM documents
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
        """, (embedding_str, embedding_str, top_k))
        
        results = cur.fetchall()
        cur.close()
        
        return results
    
    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using Gemini based on context"""
        
        if not context.strip():
            return "No relevant documents found to answer this question."
        
        prompt = f"""You are a helpful AI assistant. Based on the provided context, answer the user's question.

If the context doesn't contain relevant information, say: "The provided context does not contain information about this topic."

Context:
{context}

Question: {query}

Answer:"""
        
        try:
            response = genai.generate_text(
                prompt=prompt,
                temperature=0.7,
                max_output_tokens=300,
                model='models/text-bison-001'  # Use text-bison for text generation
            )
            return response.result if response.result else "Unable to generate answer"
        except Exception as e:
            # Fallback to chat API if text-bison fails
            try:
                model = genai.GenerativeModel('gemini-2.5-flash-lite')
                response = model.generate_content(prompt)
                return response.text
            except Exception as e2:
                print(f"Error generating answer: {e2}")
                return "Unable to generate answer"
    
    def query(self, question: str, top_k: int = 3) -> dict:
        """Complete RAG pipeline"""
        
        print(f"\n📝 Question: {question}")
        
        # Step 1: Retrieve documents
        retrieved_docs = self.retrieve_documents(question, top_k=top_k)
        
        print(f"✓ Retrieved {len(retrieved_docs)} documents")
        if len(retrieved_docs) > 0:
            for i, doc in enumerate(retrieved_docs, 1):
                print(f"  {i}. {doc['title']} (similarity: {doc['similarity']:.3f})")
        else:
            print("  ⚠️ No documents found in database!")
        
        # Step 2: Build context
        context = "\n\n".join([
            f"Document: {doc['title']}\n{doc['content']}"
            for doc in retrieved_docs
        ])
        
        # Step 3: Generate answer
        print("🤖 Generating answer...")
        answer = self.generate_answer(question, context)
        
        return {
            "question": question,
            "retrieved_documents": [
                {"title": doc["title"], "similarity": float(doc["similarity"])}
                for doc in retrieved_docs
            ],
            "answer": answer
        }
    
    def get_document_count(self) -> int:
        """Check how many documents are in database"""
        cur = self.conn.cursor()
        cur.execute("SELECT COUNT(*) as count FROM documents;")
        count = cur.fetchone()[0]  # Get the actual count value
        cur.close()
        return count
    
    def close(self):
        """Close database connection"""
        self.conn.close()


# ============================================================
# SAMPLE DATA
# ============================================================

SAMPLE_DOCUMENTS = [
    {
        "title": "Climate Change Causes",
        "content": """Climate change is primarily caused by greenhouse gas emissions from human activities.
        The main causes include:
        1. Burning fossil fuels (coal, oil, gas) for energy
        2. Industrial processes and manufacturing
        3. Deforestation and land use changes
        4. Agriculture and livestock farming
        5. Transportation and vehicle emissions

        These activities release CO2, methane, and other gases that trap heat in the atmosphere."""
    },
    {
        "title": "Renewable Energy Sources",
        "content": """Renewable energy comes from natural sources that continuously replenish.
        Main types include:
        1. Solar energy - captured from sunlight using photovoltaic panels
        2. Wind energy - generated by turbines turning with wind
        3. Hydroelectric - power from flowing or falling water
        4. Geothermal - heat from inside the Earth
        5. Biomass - energy from organic materials

        These are sustainable alternatives to fossil fuels."""
    },
    {
        "title": "Machine Learning Basics",
        "content": """Machine Learning is a subset of Artificial Intelligence that enables systems
        to learn and improve from data without explicit programming.

        Key concepts:
        1. Supervised Learning - learning from labeled data (classification, regression)
        2. Unsupervised Learning - finding patterns in unlabeled data (clustering)
        3. Reinforcement Learning - learning through rewards and penalties
        4. Neural Networks - inspired by biological neural networks
        5. Deep Learning - using multiple layers of neural networks

        Applications include image recognition, natural language processing, and recommendations."""
    },
    {
        "title": "Python Programming",
        "content": """Python is a high-level, interpreted programming language known for simplicity
        and readability. Key features:

        1. Easy syntax - readable and beginner-friendly
        2. Dynamic typing - no need to declare variable types
        3. Large standard library - built-in modules for common tasks
        4. Object-oriented - supports classes and objects
        5. Functional programming - supports lambda, map, filter
        6. Extensive ecosystem - NumPy, Pandas, Django, Flask, TensorFlow

        Python is widely used in data science, web development, and automation."""
    },
    {
        "title": "Database Optimization",
        "content": """Database optimization improves query performance and reduces resource usage.

        Key optimization techniques:
        1. Indexing - create indexes on frequently queried columns
        2. Query optimization - write efficient SQL queries
        3. Normalization - organize data to reduce redundancy
        4. Connection pooling - reuse database connections
        5. Caching - store frequently accessed data in memory
        6. Partitioning - divide large tables into smaller parts
        7. Monitoring - track performance metrics regularly

        Proper optimization can dramatically improve application performance."""
    },
    {
        "title": "Web Development with React",
        "content": """React is a JavaScript library for building user interfaces, maintained by Meta.
        Key concepts:
        1. Components - reusable UI building blocks
        2. JSX - JavaScript XML for writing HTML-like code
        3. State Management - using useState, useReducer, or Redux
        4. Props - passing data between components
        5. Hooks - functions to use state and lifecycle features
        6. Virtual DOM - efficient rendering optimization

        React enables creating interactive, dynamic web applications with component-based architecture."""
    },
    {
        "title": "Cloud Computing with AWS",
        "content": """Amazon Web Services (AWS) is a comprehensive cloud platform offering over 200 services.
        Core services include:
        1. EC2 - scalable virtual servers in the cloud
        2. S3 - object storage for any amount of data
        3. RDS - managed relational database service
        4. Lambda - serverless compute service
        5. VPC - isolated virtual networks
        6. CloudFront - content delivery network

        AWS enables businesses to build scalable, reliable applications without managing physical infrastructure."""
    },
    {
        "title": "Data Science with Pandas",
        "content": """Pandas is a Python library for data manipulation and analysis.
        Key features:
        1. DataFrame - 2D labeled data structure
        2. Series - 1D labeled array
        3. Data cleaning - handling missing values, duplicates
        4. Data filtering - selecting rows based on conditions
        5. Grouping and aggregation - summarize data
        6. Merge and join - combine multiple datasets
        7. Time series - working with date/time data

        Pandas is essential for data preprocessing, exploratory data analysis, and data wrangling."""
    },
    {
        "title": "Cybersecurity Fundamentals",
        "content": """Cybersecurity protects computer systems and networks from digital attacks.
        Key principles:
        1. CIA Triad - Confidentiality, Integrity, Availability
        2. Encryption - encoding data to prevent unauthorized access
        3. Firewalls - network security systems
        4. Authentication - verifying user identity (MFA, 2FA)
        5. Security Audits - regular security assessments
        6. Incident Response - handling security breaches

        Common threats include phishing, malware, ransomware, and social engineering attacks."""
    },
    {
        "title": "Docker and Containers",
        "content": """Docker is a platform for developing, shipping, and running applications in containers.
        Containerization benefits:
        1. Portability - runs anywhere Docker is installed
        2. Isolation - separate environments for each app
        3. Efficiency - lightweight compared to VMs
        4. Consistency - same environment across dev/prod
        5. Scalability - easy to scale horizontally

        Key concepts:
        - Dockerfile - script to build container images
        - Docker Compose - multi-container applications
        - Docker Hub - container registry
        - Volumes - persistent data storage"""
    },
    {
        "title": "Neural Networks Explained",
        "content": """Neural networks are computing systems inspired by biological neural networks.
        Architecture:
        1. Input Layer - receives initial data
        2. Hidden Layers - process information through weights and biases
        3. Output Layer - produces final predictions
        4. Activation Functions - ReLU, Sigmoid, Tanh
        5. Backpropagation - learning algorithm
        6. Gradient Descent - optimization method

        Applications: image classification, speech recognition, natural language translation, game playing."""
    },
    {
        "title": "Git Version Control",
        "content": """Git is a distributed version control system for tracking code changes.
        Essential commands:
        1. git init - initialize new repository
        2. git add - stage changes for commit
        3. git commit - save changes to history
        4. git push - upload changes to remote
        5. git pull - download changes from remote
        6. git branch - create separate lines of development
        7. git merge - combine branches together

        Git enables collaboration, experimentation, and rollback capabilities for software projects."""
    },
    {
        "title": "API Development with FastAPI",
        "content": """FastAPI is a modern, fast Python web framework for building APIs.
        Key features:
        1. Automatic API documentation - OpenAPI and JSON Schema
        2. Type hints - better code quality and IDE support
        3. Async support - high performance with async/await
        4. Data validation - using Pydantic models
        5. Dependency injection - clean, testable code
        6. Authentication - built-in security features

        FastAPI is ideal for building RESTful APIs, microservices, and backend services."""
    },
    {
        "title": "Natural Language Processing",
        "content": """NLP enables computers to understand, interpret, and generate human language.
        Key techniques:
        1. Tokenization - splitting text into words/tokens
        2. Word Embeddings - Word2Vec, GloVe, BERT
        3. Sentiment Analysis - determining emotional tone
        4. Named Entity Recognition - identifying people, places, organizations
        5. Machine Translation - translating between languages
        6. Text Generation - creating human-like text

        Applications: chatbots, translation services, sentiment analysis, text summarization."""
    },
    {
        "title": "Kubernetes Orchestration",
        "content": """Kubernetes (K8s) is a container orchestration platform for managing containerized workloads.
        Core features:
        1. Pods - smallest deployable units
        2. Services - stable network endpoints
        3. Deployments - managing application updates
        4. ConfigMaps - configuration data
        5. Secrets - sensitive data management
        6. Ingress - HTTP/HTTPS routing
        7. Auto-scaling - adjusting resources based on demand

        Kubernetes provides self-healing, scaling, and management for containerized applications."""
    }
]


# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("="*60)
    print("🍽️ FIXED RAG PIPELINE WITH DATA LOADING")
    print("="*60)
    
    # Initialize RAG
    rag = FixedRAGPipeline()
    
    # Check current document count
    current_count = rag.get_document_count()
    print(f"📊 Current documents in database: {current_count}")

    # Load sample documents (clear and reload for fresh data)
    print("\n📝 Clearing existing documents and reloading fresh data...")
    cur = rag.conn.cursor()
    cur.execute("DELETE FROM documents;")
    rag.conn.commit()
    cur.close()
    print(f"  ✓ Cleared {current_count} old documents")

    print("📥 Loading new sample documents...")
    loaded = rag.load_documents(SAMPLE_DOCUMENTS)
    
    # Verify documents loaded
    final_count = rag.get_document_count()
    print(f"📊 Final document count: {final_count}\n")
    
    # Test queries
    # test_queries = [
    #     "What are the main causes of climate change?",
    #     "How does React work for web development?",
    #     "What is Docker and why use containers?",
    #     "Tell me about neural networks",
    #     "How does Kubernetes help with container orchestration?",
    #     "What are the main AWS cloud services?",
    #     "How does Git version control work?",
    #     "Explain FastAPI for building APIs"
    # ]
    
    # print("="*60)
    # print("TESTING RAG PIPELINE")
    # print("="*60)
    
    # for query in test_queries:
    #     result = rag.query(query)
    #     print(f"\n{'='*60}")
    #     print(f"Answer: {result['answer']}")
    
    # Close connection
    rag.close()
    print("\n✅ RAG Pipeline test completed!")
