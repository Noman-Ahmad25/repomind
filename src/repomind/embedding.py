from typing import List, Any, cast
from sentence_transformers import SentenceTransformer 
# Our designated local model
MODEL_NAME = "BAAI/bge-small-en-v1.5"
_model = None

def get_model() -> Any:
    """Lazy load the model so the CLI doesn't hang on startup."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model

def chunk_text(text: str, max_chars: int = 1500, overlap: int = 200) -> List[str]:
    """Break text into overlapping chunks to preserve context."""
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + max_chars
        chunks.append(text[start:end])
        start += max_chars - overlap
        
    return chunks

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """Convert text chunks into 768-dimensional vectors."""
    if not texts:
        return []
    
    model = get_model()
    # Convert numpy arrays to standard python lists for future database storage
    embeddings = model.encode(texts, normalize_embeddings=True)
    return cast(List[List[float]], embeddings.tolist())
