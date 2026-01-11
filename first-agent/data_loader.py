# 2_data_loader.py
from pathlib import Path
import os

class SimpleDocumentLoader:
    """Load documents from text files"""
    
    @staticmethod
    def load_from_directory(directory_path: str) -> list[dict]:
        """
        Load all .txt files from a directory
        Returns: List of dicts with 'title' and 'content'
        """
        documents = []
        path = Path(directory_path)
        
        for file_path in path.glob("*.txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                documents.append({
                    "title": file_path.stem,
                    "content": f.read()
                })
        
        return documents
    
    @staticmethod
    def load_from_list(doc_list: list[dict]) -> list[dict]:
        """
        Load documents from a list
        Expected format: [{"title": "...", "content": "..."}, ...]
        """
        return doc_list

# Example usage
sample_documents = [
    {
        "title": "Climate Change Facts",
        "content": """Climate change refers to long-term shifts in temperatures and 
        weather patterns. The main cause is human activity, particularly the emission 
        of greenhouse gases like carbon dioxide. Rising temperatures lead to melting 
        ice caps, sea level rise, and more frequent extreme weather events."""
    },
    {
        "title": "Renewable Energy",
        "content": """Renewable energy comes from natural sources like sun, wind, water, 
        and geothermal heat. Solar panels convert sunlight into electricity. Wind turbines 
        generate power from wind. These energy sources reduce carbon emissions and are 
        sustainable for the long term."""
    },
    {
        "title": "AI Technology",
        "content": """Artificial Intelligence is transforming industries. Machine learning 
        models learn from data to make predictions. Deep learning uses neural networks 
        inspired by the brain. NLP (Natural Language Processing) enables computers to 
        understand human language. Computer vision allows machines to interpret images."""
    }
]

if __name__ == "__main__":
    loader = SimpleDocumentLoader()
    docs = loader.load_from_list(sample_documents)
    print(f"Loaded {len(docs)} documents")
    for doc in docs:
        print(f"- {doc['title']}: {len(doc['content'])} chars")
