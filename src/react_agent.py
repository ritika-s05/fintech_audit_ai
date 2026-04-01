import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.retriever import search
from src.llm import chat

def agent(question: str, max_steps: int = 3) -> str:
    """
    ReAct agent — Reason + Act loop.
    
    Each step the agent:
    1. THINKS about what it needs to find
    2. SEARCHES the vector store
    3. OBSERVES the results
    4. Decides if it has enough to answer or needs another search
    """

    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")

    history = []   # keeps track of all steps
    
    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step} ---")

        # Step 1 — ask LLM what to search for
        history_text = "\n".join(history) if history else "No previous searches."
        
        think_prompt = f"""You are a financial research agent answering this question:
"{question}"

Previous steps:
{history_text}

What specific phrase should you search for next to find relevant information ?
Reply with ONLY the search query, notghing else. Keeping it under 10 words. """

        search_query = chat(prompt=think_prompt)
        print(f" Searching for: '{search_query}'")

        #search
        results = search(search_query, n_results=3)
        chunks = results["documents"][0]
        companies = [m["company"] for m in results["metadatas"][0]]

        #observe
        observations = ""
        for chunk, company in zip(chunks, companies):
            observations += f"[{company}]: {chunk[:300]}\n \n"

        history.append(f"Step{step} - Searched: '{search_query}'\nFound: {observations[:500]}")
        print(f"Retrieved {len(chunks)} chunks")

        #decide if we have enough
        decide_prompt = f"""You are answering: "{question}"

Information gathered so far:
{chr(10).join(history)}

Do you have enough information to give a complete answer?
Reply with just YES or NO."""

        decision = chat(prompt=decide_prompt).strip().upper()
        print(f"Enough info? {decision}")

        if "YES" in decision:
            break
    
    #final answer
    final_prompt = f"""Using the research below, give a clear and detailed answer to:
"{question}"

Research:
{chr(10).join(history)}

Give a well structed answer with specific details from the filings."""


    print(f"\n Generating final answer...\n")
    answer = chat(prompt=final_prompt, system="You are a financial analyst. Be factual and specific.")
    return answer


if __name__ == "__main__":
    questions = [
        "Compare how JPMorgan and Goldman Sachs manage risk differently?",
        "What are the biggest challenges facing Bank of America in 2025?",
    ]

    for q in questions:
        answer = agent(q)
        print(f"\n{'='*60}")
        print(f"FINAL ANSWER:\n{answer}")
        print(f"{'='*60}\n")
