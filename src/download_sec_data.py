import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

RAW_DATA_PATH = os.getenv("DATA_RAW_PATH", "./data/raw")
os.makedirs(RAW_DATA_PATH, exist_ok=True)

# SEC requires a User-Agent header to identify yourself
HEADERS = {
    "User-Agent": "Ritika sisodiyaritika511@gmail.com",
    "Accept-Encoding": "gzip, deflate",
}

def get_company_filings(cik: str, form_type: str = "10-K", count: int = 3):
    """
    Fetch filing metadata for a company from SEC EDGAR.
    CIK = Central Index Key (unique company ID on EDGAR)
    """
    url = f"https://data.sec.gov/submissions/CIK{cik.zfill(10)}.json"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    filings = data["filings"]["recent"]
    results = []

    for i, form in enumerate(filings["form"]):
        if form == form_type:
            results.append({
                "company":      data["name"],
                "cik":          cik,
                "form":         form,
                "filed":        filings["filingDate"][i],
                "accession":    filings["accessionNumber"][i],
                "primaryDoc":   filings["primaryDocument"][i],
            })
        if len(results) == count:
            break

    return results

def download_filing(filing: dict):
    """
    Download the actual PDF/HTML filing document.
    """
    accession = filing["accession"].replace("-", "")
    cik = filing["cik"].zfill(10)
    doc = filing["primaryDoc"]

    url = f"https://www.sec.gov/Archives/edgar/data/{int(filing['cik'])}/{accession}/{doc}"
    
    response = requests.get(url, headers=HEADERS)
    time.sleep(0.5)  # SEC rate limit — be polite!

    # save to data/raw/
    clean_name = "".join(c if c.isalnum() or c in "_-" else "_" for c in filing['company'])
    filename = f"{clean_name}_{filing['form']}_{filing['filed']}.html"
    filepath = os.path.join(RAW_DATA_PATH, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    print(f"Downloaded: {filename}")
    return filepath

if __name__ == "__main__":
    # Some well-known financial companies and their SEC CIK numbers
    companies = {
        "JPMorgan Chase": "0000019617",
        "Goldman Sachs":  "0000886982",
        "Bank of America":"0000070858",
    }

    all_filings = []
    for company, cik in companies.items():
        print(f"\n🔍 Fetching filings for {company}...")
        filings = get_company_filings(cik, form_type="10-K", count=1)
        all_filings.extend(filings)

    print(f"\n📥 Downloading {len(all_filings)} filings...\n")
    for filing in all_filings:
        download_filing(filing)

    print(f"\n✅ Done! Files saved to {RAW_DATA_PATH}")