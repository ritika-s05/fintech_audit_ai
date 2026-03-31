import os

PROCESSED_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "processed")

def chunk_text(text: str, chunk_size: int = 500, overlap: int=50) -> list:
    """
    Split text into overlapping chunks.

    chunk_size: number of words per chunk
    overlap:  number of words shared between consecutive chunks
            (so context isn't lost at chunk boundaries)
    """

    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap 
    
    return chunks

def filter_chunks(chunks: list) -> list:
    """Remove low-quality chunks (XBRL metadata, too short, mostly URLs)."""
    clean = []
    for chunk in chunks:
        # skip if too many http links
        if chunk.count("http") > 5:
            continue
        # skip if too short
        if len(chunk.split()) < 30:
            continue
        # skip XBRL metadata chunks
        if chunk.count("us-gaap:") > 3:
            continue
        if chunk.count("0000") > 3:
            continue
        clean.append(chunk)
    return clean

if __name__ == "__main__":
    for filename in os.listdir(PROCESSED_DATA_PATH):
        if filename.endswith(".txt"):
            filepath = os.path.join(PROCESSED_DATA_PATH, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()

            chunks = chunk_text(text)
            chunks = filter_chunks(chunks)  # ← this line must be here
            print(f"{filename}")
            print(f"  Total words:  {len(text.split())}")
            print(f"  Total chunks: {len(chunks)}")
            print(f"  First chunk preview:\n")
            print(f"  {chunks[0][:300]}\n")