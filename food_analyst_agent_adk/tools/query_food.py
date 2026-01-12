"""Food Query Tool for ADK - Indonesian Menu Analysis"""
import os
from typing import Dict, Any, List


def query_food(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Query the food database to retrieve relevant Indonesian menus based on preferences.

    Args:
        query: The food preference, dietary requirement, or menu description
        top_k: Number of relevant menus to retrieve (default: 3)

    Returns:
        Dictionary containing:
            - query: The original query
            - retrieved_menus: List of retrieved menus with nutritional info
            - context: Formatted context string from retrieved menus
            - success: Boolean indicating if the query was successful
            - error: Error message if unsuccessful
    """
    try:
        from ..core import FoodPipeline

        # Initialize food pipeline
        food_pipeline = FoodPipeline()

        # Retrieve similar menus
        retrieved_menus = food_pipeline.retrieve_similar_menus(query, top_k=top_k)

        # Close the connection
        food_pipeline.close()

        # Build context from retrieved menus - CHANGED FORMAT
        context = "\n\n".join([
            f"""Menu: {menu['nama_menu']}
Kategori: {menu['kategori']}
Asal: {menu['asal']}
Deskripsi: {menu['deskripsi']}
Nutrisi per porsi:
  - Kalori: {menu['kalori']} kcal
  - Protein: {menu['protein']}g
  - Lemak: {menu['lemak']}g
  - Karbohidrat: {menu['karbohidrat']}g
  - Serat: {menu['serat']}g
Tingkat Kesehatan: {menu['tingkat_kesehatan']}
Harga: {menu['harga']}
Cocok untuk: {', '.join(menu['cocok_untuk'])}
Similarity Score: {menu['similarity']:.2f}"""
            for menu in retrieved_menus
        ])

        return {
            "query": query,
            "retrieved_menus": [
                {
                    "nama": menu["nama_menu"],
                    "kalori": menu["kalori"],
                    "protein": menu["protein"],
                    "kesehatan": menu["tingkat_kesehatan"],
                    "harga": menu["harga"],
                    "similarity": float(menu["similarity"])
                }
                for menu in retrieved_menus
            ],
            "context": context,
            "success": True,
            "num_results": len(retrieved_menus)
        }

    except Exception as e:
        return {
            "query": query,
            "success": False,
            "error": str(e),
            "retrieved_menus": [],
            "context": ""
        }
