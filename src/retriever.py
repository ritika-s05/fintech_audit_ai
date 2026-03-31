import os
import sys
import chromadb
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.embedder import embed
from src.chunker import chunk_text, filter_chunks

VECTORSTORE_PATH = os.getenv("VECTORSTORE_PATH", "./vectorstore")
PROCESSED_DATA_PATH = "./data/processed"

client = chromadb.PersistentClient(path=VECTORSTORE_PATH)

def get_collection(name: str = "sec_filings"):
    return client.get_or_create_collection(name=name)

def index_documents():
    collection  = get_collection()
    for filename in os.listdir(PROCESSED_DATA_PATH):
        if not filename.endswith(".txt"):
            continue
        filepath = os.path.join(PROCESSED_DATA_PATH, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()

        chunks = filter_chunks(chunk_text(text))
        company = filename.replace(".txt", "")
        print(f"Indexing {company} — {len(chunks)} chunks...")

        embeddings = embed(chunks)
        collection.add(
            documents=chunks,
            embeddings=embeddings.tolist(),
            ids=[f"{company}_chunk_{i}" for i in range(len(chunks))],
            metadatas=[{"company": company} for _ in chunks],
        )
        print(f"✅ Indexed {len(chunks)} chunks\n")

def search(query: str, n_results: int = 5):
    collection = get_collection()
    query_embedding = embed([query])[0].tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )
    return results

if __name__ == "__main__":
    print("Building vector store...\n")
    index_documents()

    print("\n🔍 Test search: 'What are the main risks for JPMorgan?'\n")
    results = search("What are the main risks for JPMorgan?")
    for i, doc in enumerate(results["documents"][0]):
        company = results["metadatas"][0][i]["company"]
        print(f"Result {i+1} [{company}]:\n{doc[:300]}\n")