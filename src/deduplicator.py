import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from rapidfuzz import fuzz
from src.embedder import embed, cosine_similarity

OUTPUT_PATH = "./outputs"
os.makedirs(OUTPUT_PATH, exist_ok=True)

def fuzzy_match_names(names: list, threshold: float = 80.0) -> list:
    """
    Find all pairs of names that are fuzzy-similar above the threshold.
    Returns list of (index_a, index_b, score) tuples.
    """
    matches = []
    for i, name_a in enumerate(names):
        for j, name_b in enumerate(names):
            if j <= i:
                continue
            score = fuzz.token_sort_ratio(name_a, name_b)
            if score >= threshold:
                matches.append((i, j, score))
    return sorted(matches, key=lambda x: -x[2])

def embedding_match_names(names: list, threshold: float = 0.85) -> list:
    """
    Find similar names using semantic embeddings.
    Returns list of (index_a, index_b, similarity) tuples.
    """
    embeddings = embed(names)
    matches = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            sim = cosine_similarity(embeddings[i], embeddings[j])
            if sim >= threshold:
                matches.append((i, j, round(sim, 4)))
    return sorted(matches, key=lambda x: -x[2])


##Duplication Pipeline

def find_duplicates(df: pd.DataFrame, name_col: str ="company",
                    fuzzy_threshold: float = 80.0,
                    embed_threshold: float = 0.85) -> pd.DataFrame:
    """
    Full deduplication pipeline on a DataFrame.
    Returns DataFrame of suspected duplicate pairs.
    """

    names = df[name_col].fillna("").tolist()
    print(f"Running deduplication on {len(names)} records...")

    #fuzzy matches
    print("  Stage 1: Fuzzy string matching...")
    fuzzy_matches = fuzzy_match_names(names, fuzzy_threshold)
    fuzzy_pairs = {(i, j) for i, j, _ in fuzzy_matches}

    #embedding matching
    print("Stage 2: Embedding similarity...")
    emed_matches = embedding_match_names(names, embed_threshold)
    emed_pairs = {(i, j) for i, j, _ in emed_matches}

    #combining both

    all_pairs = fuzzy_pairs.union(emed_pairs)
    fuzzy_score_map = {(i, j): s for i, j, s in fuzzy_matches}
    embed_score_map = {(i, j): s for i, j, s in emed_matches}

    rows = []
    for i, j in all_pairs:
        rows.append({
            "index_a":       i,
            "index_b":       j,
            "name_a":        names[i],
            "name_b":        names[j],
            "fuzzy_score":   fuzzy_score_map.get((i, j), 0),
            "embedding_sim": embed_score_map.get((i, j), 0.0),
            "flagged_by":    "both" if (i,j) in fuzzy_pairs and (i,j) in emed_pairs
                            else "fuzzy" if (i,j) in fuzzy_pairs else "embedding",

        })

    results_df = pd.DataFrame(rows)
    print(f"Found{len(results_df)} potential duplicate pairs. \n")
    return results_df

def deduplicate(df: pd.DataFrame, duplicates_df: pd.DataFrame,
                threshold: float = 90.0 ) -> pd.DataFrame:
    """Remove high confidemce duplicates from the DataFrame."""
    high_conf = duplicates_df[duplicates_df["fuzzy_score"] >= threshold]
    indices_to_drop = set(high_conf["index_b"].tolist())
    cleaned = df.drop(index=indices_to_drop).reset_index(drop=True)
    print(f"Original rows: {len(df)}")
    print(f"Dropped: {len(indices_to_drop)} duplicates")
    print(f"Cleaned rows: {len(cleaned)}")
    return cleaned

if __name__ == "__main__":

    #creating messy excle with duplicates
    data = {
        "company":      ["JPMorgan Chase", "Goldman Sachs", "Bank of America",
                         "JP Morgan Chase", "Goldman Sachs Group", "Bank of America Corp",
                         "JPMorgan", "GS Group", "BofA"],
        "revenue":      ["$158B", "$58B", "$98B",
                         "$158B", "$58B", "$98B",
                         "$158B", "$58B", "$98B"],
        "fiscal_year":  ["2025"] * 9,
    }
    df = pd.DataFrame(data)

    # save messy sheet
    messy_path = "./outputs/companies_messy.xlsx"
    df.to_excel(messy_path, index=False)
    print(f"📊 Messy sheet saved → {messy_path}\n")

    # find duplicates
    duplicates_df = find_duplicates(df, name_col="company")
    print(duplicates_df[["name_a", "name_b", "fuzzy_score", "embedding_sim", "flagged_by"]])

    # save duplicates report
    duplicates_df.to_excel("./outputs/duplicates_report.xlsx", index=False)
    print("\n📊 Duplicates report saved → outputs/duplicates_report.xlsx")

    # deduplicate
    print("\n🧹 Deduplicating...")
    cleaned_df = deduplicate(df, duplicates_df)
    cleaned_df.to_excel("./outputs/companies_clean.xlsx", index=False)
    print(" Clean sheet saved → outputs/companies_clean.xlsx")




