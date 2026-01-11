"""RAG Agent using Google ADK"""
import os
from dotenv import load_dotenv
from google.adk.agents.llm_agent import LlmAgent

# Load environment variables
load_dotenv()

from .tools.query_rag import query_rag


# Create the agent
root_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="rag_agent",
    instruction="""You are a helpful RAG (Retrieval-Augmented Generation) assistant that helps users find information from a document database.

When users ask questions:

1. Use the query_rag tool to search the document database for relevant information
2. The tool will return relevant documents with similarity scores
3. Provide a helpful answer based on the retrieved context
4. If no relevant documents are found (low similarity scores or empty results), let the user know
5. Always be conversational and cite which documents you used in your answer

Example queries:
- "What are the main causes of climate change?"
- "How does renewable energy work?"
- "What is machine learning?"

Your goal is to provide accurate, context-aware answers based on the retrieved documents.""",
    tools=[query_rag]
)
