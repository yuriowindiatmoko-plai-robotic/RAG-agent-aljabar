"""RAG Query Tool for ADK"""
import os
from typing import Dict, Any, List


def query_rag(query: str, top_k: int = 3) -> Dict[str, Any]:
    """
    Query the RAG system to retrieve relevant documents based on a question.

    Args:
        query: The question or query to search for
        top_k: Number of relevant documents to retrieve (default: 3)

    Returns:
        Dictionary containing:
            - query: The original query
            - retrieved_documents: List of retrieved documents with titles and similarity scores
            - context: Formatted context string from retrieved documents
            - success: Boolean indicating if the query was successful
            - error: Error message if unsuccessful
    """
    try:
        from ..core import RAGPipeline

        # Initialize RAG pipeline
        rag = RAGPipeline()

        # Retrieve similar documents
        retrieved_docs = rag.retrieve_similar_documents(query, top_k=top_k)

        # Close the connection
        rag.close()

        # Build context from retrieved documents
        context = "\n\n".join([
            f"Document: {doc['title']}\n{doc['content']}"
            for doc in retrieved_docs
        ])

        return {
            "query": query,
            "retrieved_documents": [
                {
                    "title": doc["title"],
                    "similarity": float(doc["similarity"]),
                    "content": doc["content"][:200] + "..." if len(doc["content"]) > 200 else doc["content"]
                }
                for doc in retrieved_docs
            ],
            "context": context,
            "success": True,
            "num_results": len(retrieved_docs)
        }

    except Exception as e:
        return {
            "query": query,
            "success": False,
            "error": str(e),
            "retrieved_documents": [],
            "context": ""
        }
