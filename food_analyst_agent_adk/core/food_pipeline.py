"""Food Pipeline core logic for Indonesian cuisine analysis"""
from sentence_transformers import SentenceTransformer
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Dict, Any
import os


class FoodPipeline:
    """Food analyst pipeline for Indonesian menu retrieval and nutritional analysis"""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """Initialize food pipeline with embedding model and database connection"""
        # Initialize embedding model (same as reference: all-MiniLM-L6-v2)
        self.embedding_model = SentenceTransformer(model_name, device='cpu')

        # Database connection
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "boilerplate"),
            password=os.getenv("DB_PASSWORD", "boilerplate"),
            database=os.getenv("DB_NAME", "boilerplate_db"),
            port=int(os.getenv("DB_PORT", 5432))
        )
        self.conn.autocommit = True

    def retrieve_similar_menus(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Find most similar Indonesian menus to the query"""
        # Generate query embedding (384 dimensions)
        query_embedding = self.embedding_model.encode(query)

        # Convert to string format for pgvector
        embedding_str = "[" + ",".join([str(x) for x in query_embedding]) + "]"

        # Similarity search in PostgreSQL - CHANGED TABLE & FIELDS
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        search_query = f"""
            SELECT
                id,
                nama_menu,
                kategori,
                asal,
                deskripsi,
                kalori,
                protein,
                lemak,
                karbohidrat,
                serat,
                garam,
                tingkat_kesehatan,
                harga,
                cocok_untuk,
                1 - (embedding <=> '{embedding_str}'::vector) as similarity
            FROM food_menu
            ORDER BY embedding <=> '{embedding_str}'::vector
            LIMIT {top_k}
        """

        cur.execute(search_query)
        results = cur.fetchall()
        cur.close()

        return results

    def get_nutrition_by_name(self, menu_name: str) -> Dict[str, Any]:
        """Get complete nutritional information for a specific menu"""
        cur = self.conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "SELECT * FROM food_menu WHERE nama_menu ILIKE %s",
            (f"%{menu_name}%",)
        )
        result = cur.fetchone()
        cur.close()

        if not result:
            return {"error": "Menu not found"}

        # Calculate daily percentages based on 2000 kcal diet
        daily_needs = {
            "kalori": 2000,
            "protein": 50,
            "lemak": 70,
            "karbohidrat": 300
        }

        return {
            "menu": result['nama_menu'],
            "nutrition": {
                "kalori": {
                    "nilai": result['kalori'],
                    "persen_harian": round(result['kalori'] / daily_needs['kalori'] * 100, 1)
                },
                "protein": {
                    "gram": result['protein'],
                    "persen_harian": round(result['protein'] / daily_needs['protein'] * 100, 1)
                },
                "lemak": {
                    "gram": result['lemak'],
                    "persen_harian": round(result['lemak'] / daily_needs['lemak'] * 100, 1)
                },
                "karbohidrat": {
                    "gram": result['karbohidrat'],
                    "persen_harian": round(result['karbohidrat'] / daily_needs['karbohidrat'] * 100, 1)
                },
                "serat": result['serat'],
                "garam": result['garam']
            },
            "metadata": {
                "kategori": result['kategori'],
                "asal": result['asal'],
                "tingkat_kesehatan": result['tingkat_kesehatan'],
                "harga": result['harga'],
                "cocok_untuk": result['cocok_untuk']
            }
        }

    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()
