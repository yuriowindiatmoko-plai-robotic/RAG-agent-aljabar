"""
Script 1: Create food_menu table for Food Analyst Agent
Run with: python scripts/1_create_table.py
"""
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables from food_analyst_agent_adk/.env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'food_analyst_agent_adk', '.env'))


def create_food_menu_table():
    """Create the food_menu table with all necessary columns and indexes"""
    
    # Database connection parameters
    db_params = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "boilerplate"),
        "password": os.getenv("DB_PASSWORD", "boilerplate"),
        "database": os.getenv("DB_NAME", "boilerplate_db"),
        "port": int(os.getenv("DB_PORT", 5432))
    }
    
    print(f"Connecting to database: {db_params['database']} at {db_params['host']}:{db_params['port']}")
    
    try:
        # Connect to database
        conn = psycopg2.connect(**db_params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # SQL to create the food_menu table
        create_table_sql = """
        -- Drop table if exists (optional - comment out if you want to preserve existing data)
        -- DROP TABLE IF EXISTS public.food_menu;

        CREATE TABLE IF NOT EXISTS public.food_menu_2 (
            id serial4 NOT NULL,
            nama_menu text NULL,
            kategori text NULL,
            asal text NULL,
            deskripsi text NULL,
            kalori int4 NULL,
            protein int4 NULL,
            lemak int4 NULL,
            karbohidrat int4 NULL,
            serat int4 NULL,
            garam float8 NULL,
            tingkat_kesehatan text NULL,
            harga text NULL,
            cocok_untuk _text NULL,
            embedding public.vector NULL,
            created_at timestamp DEFAULT CURRENT_TIMESTAMP NULL,
            CONSTRAINT food_menu_2_nama_menu_key UNIQUE (nama_menu),
            CONSTRAINT food_menu_2_pkey PRIMARY KEY (id)
        );
        """
        
        # Execute create table
        print("Creating food_menu table...")
        cursor.execute(create_table_sql)
        print("✓ Table created successfully!")
        
        # Create indexes
        indexes_sql = [
            """
            CREATE INDEX IF NOT EXISTS food_menu_2_embedding_idx 
            ON public.food_menu_2 USING ivfflat (embedding vector_cosine_ops) 
            WITH (lists='100');
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_kalori 
            ON public.food_menu_2 USING btree (kalori);
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_kategori 
            ON public.food_menu_2 USING btree (kategori);
            """
        ]
        
        print("Creating indexes...")
        for idx_sql in indexes_sql:
            try:
                cursor.execute(idx_sql)
            except psycopg2.Error as e:
                # Ignore if index already exists
                if "already exists" not in str(e):
                    print(f"  Warning: {e}")
        print("✓ Indexes created successfully!")
        
        # Verify table exists
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'food_menu_2'
            ORDER BY ordinal_position;
        """)
        columns = cursor.fetchall()
        
        print("\n📋 Table structure:")
        print("-" * 40)
        for col_name, data_type in columns:
            print(f"  {col_name}: {data_type}")
        print("-" * 40)
        
        cursor.close()
        conn.close()
        print("\n✅ food_menu table is ready!")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise


if __name__ == "__main__":
    create_food_menu_table()
