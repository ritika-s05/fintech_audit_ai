import os
from bs4 import BeautifulSoup

RAW_DATA_PATH = "./data/raw"
PROCESSED_DATA_PATH = "./data/processed"
os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

def parse_html_filing(filepath: str) -> str:
    with open(filepath, "rb") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

#removing noise
    for tag in soup(["script", "style", "table"]):
        tag.decompose()

    text = soup.get_text(separator="\n")

    # clean up blank lines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return "\n".join(lines)

if __name__ == "__main__":
    for filename in os.listdir(RAW_DATA_PATH):
        if filename.endswith(".html"):
            filepath = os.path.join(RAW_DATA_PATH, filename)
            print(f"Parsing {filename}...")
            text = parse_html_filing(filepath)

            out_filename = filename.replace(".html", ".txt")
            out_path = os.path.join(PROCESSED_DATA_PATH, out_filename)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Saved: {out_filename} ({len(text)} chars)\n")

