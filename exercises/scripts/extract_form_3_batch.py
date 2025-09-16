# scripts/extract_form_3_batch.py
import os
import json
import pandas as pd
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# -------- Structured output model --------
class Form3Filing(BaseModel):
    insider_name: str
    insider_role: List[str]
    company_name: str
    company_cik: str
    filing_date: str

# -------- Config / inputs --------
CSV_PATH = "/scratch/shared/yens-onboarding-2025/data/form_3_100.csv"
ENV_PATH = "/scratch/shared/yens-onboarding-2025/.env"
OUTPUT_PATH = "results/form3_batch_results.json"

# -------- Setup --------
load_dotenv(ENV_PATH)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv(CSV_PATH)
filepaths = df["filepath"].tolist()

system_prompt = """
You are a data extraction agent for SEC Form 3 filings.

Extract the following fields:

- insider_name: The name of the insider (from reportingOwner or anywhere in the document).
- insider_role: A list of roles the insider holds (Director, Officer, 10% Owner, Other).
- company_name: The issuer's company name.
- company_cik: The CIK number of the issuer (from issuerCik or COMPANY DATA).
- filing_date: The filing date (prefer signatureDate or FILED AS OF DATE).

Return valid JSON matching the provided Pydantic model.
"""

# -------- Process sequentially  --------
results = []

print(f"Processing {len(filepaths)} filings...")

for path in filepaths:
    with open(path, "r") as f:
        filing_text = f.read()
    print(f"Processing file {path}")
    response = client.responses.parse(
        model="gpt-4.1-nano",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": filing_text},
        ],
        text_format=Form3Filing,
    )

    parsed = response.output_parsed.model_dump()
    parsed["filing_path"] = path
    results.append(parsed)

# -------- Save results once at the end --------
os.makedirs("results", exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(results, f, indent=2)

print(f"Saved {len(results)} records to {OUTPUT_PATH}")

