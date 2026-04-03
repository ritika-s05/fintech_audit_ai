import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.retriever import search
from src.llm import chat

# Fields we want to extract from each 10-K filing
EXTRACTION_FIELDS = {
    "company_name":   "What is the full legal name of the company?",
    "fiscal_year":    "What fiscal year does this report cover?",
    "total_revenue":  "What is the total revenue or net revenue for the year?",
    "net_income":     "What is the net income or net earnings for the year?",
    "total_assets":   "What are the total assets of the company?",
    "key_risks":      "What are the top 3 main risks mentioned?",
    "ceo_name":       "Who is the CEO or Chief Executive Officer?",
    "headquarters":   "Where is the company headquartered?",
}

def extract_field(field: str, question: str, company_filter: str = None) -> str:
    """
    Extract a specific field from the filing using RAG + LLM.
    
    Args:
        field:          The field name we're extracting
        question:       The question to search for
        company_filter: Optional company name to filter results
    """
    # search for relevant chunks
    results = search(question, n_results=3)
    chunks = results["documents"][0]
    metadatas = results["metadatas"][0]

    # filter by company if specified
    if company_filter:
        filtered = [
            chunk for chunk, meta in zip(chunks, metadatas)
            if company_filter.lower() in meta["company"].lower()
        ]
        chunks = filtered if filtered else chunks

    context = "\n\n".join(chunks)

    prompt = f"""Extract the following information from this SEC 10-K filing excerpt:

FIELD: {field}
QUESTION: {question}

FILING EXCERPT:
{context}

Reply with ONLY the extracted value, nothing else. If not found, reply with 'Not found'.
Keep your answer concise — one sentence or number maximum."""

    return chat(prompt=prompt)


def extract_company_profile(company_name: str) -> dict:
    """
    Extract all fields for a given company.
    Returns a dictionary of extracted fields.
    """
    print(f"\n📄 Extracting profile for: {company_name}")
    profile = {"company": company_name}

    for field, question in EXTRACTION_FIELDS.items():
        print(f"  Extracting {field}...")
        value = extract_field(field, question, company_filter=company_name)
        profile[field] = value

    return profile


def save_to_excel(profiles: list, output_path: str = "./outputs/company_profiles.xlsx"):
    """Save extracted profiles to Excel."""
    import pandas as pd
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df = pd.DataFrame(profiles)
    df.to_excel(output_path, index=False)
    print(f"\n Saved to {output_path}")
    return df


if __name__ == "__main__":
    companies = [
        "JPMORGAN",
        "GOLDMAN_SACHS",
        "BANK_OF_AMERICA",
    ]

    all_profiles = []
    for company in companies:
        profile = extract_company_profile(company)
        all_profiles.append(profile)
        print(f"\n {company} done!")
        print(json.dumps(profile, indent=2))

    print("\n📊 Saving all profiles to Excel...")
    save_to_excel(all_profiles)