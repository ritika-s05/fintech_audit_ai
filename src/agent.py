import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.retriever import search
from src.llm import chat

def ask(question: str, n_chunks: int= 5) -> str:
    #retrieve relevant chunks
    print(f"\n Searching for: '{question}'")
    results = search(question, n_results=n_chunks)
    chunks = results["documents"][0]
    companies = [m["company"] for m in results["metadatas"][0]]

    #build context from chunks
    context = ""
    for i,(chunk, company) in enumerate(zip(chunks, companies)):
        context += f"\n [Source {i+1} - {company}]\n{chunk}\n"

    #ask llm to answer using the content
    system = "You are a financial analyst assistant. Answer questions using only the provided context from SEC filings. Be concise and factual."

    prompt = f"""Use the following excerpts from real SEC 10-K filings to answer the question.

CONTEXT:
{context}

QUESTION: {question}

ANSWER:"""

    print("🤖 Thinking...\n")
    answer = chat(prompt=prompt, system=system)
    return answer


if __name__ == "__main__":
    questions = [
        "What are the main risks for JPMorgan?",
        "How does Goldman Sachs manage market risk?",
        "What is Bank of America's strategy for growth?",
    ]

    for question in questions:
        print(f"\n{'='*60}")
        print(f"Q: {question}")
        print(f"{'='*60}")
        answer = ask(question)
        print(f"A: {answer}")