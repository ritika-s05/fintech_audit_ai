import os
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

_model = None

def get_model():
    global _model
    if _model is None:
        print(f"Loading embedding model: {MODEL_NAME}...")
        _model = SentenceTransformer(MODEL_NAME)
        print("Model loaded.")
    return _model

def embed(texts: list) -> np.ndarray:
    model = get_model()
    return model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))

if __name__ == "__main__":
    test = [
        "JPMorgan total revenue 2025",
        "Goldman Sachs risk management",
        "Bank of America loan portfolio",
        "What is the weather today",   # unrelated — should score low
    ]

    print("Embedding test sentences...\n")
    embeddings = embed(test)
    print(f"\nEmbedding shape: {embeddings.shape}")
    print(f"\nSimilarity to 'JPMorgan total revenue 2025':")
    for i, sentence in enumerate(test):
        sim = cosine_similarity(embeddings[0], embeddings[i])
        print(f"  {sentence:<45} → {sim:.4f}")
