# scripts/extract_form_3_batch_checkpoint.py
import os
import json
import pandas as pd
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

# ---------- Schema ----------
class Form3Filing(BaseModel):
    insider_name: str
    insider_role: List[str]
    company_name: str
    company_cik: str
    filing_date: str

# ---------- Config ----------
CSV_PATH = "/scratch/shared/yens-onboarding-2025/data/form_3_100.csv"
ENV_PATH = "/scratch/shared/yens-onboarding-2025/.env"
OUT_JSON = "results/form3_batch.json"

# ---------- Setup ----------
os.makedirs("results", exist_ok=True)
load_dotenv(ENV_PATH)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

df = pd.read_csv(CSV_PATH)
filepaths = df["filepath"].tolist()

# Load previous results (to resume)
results = []
if os.path.exists(OUT_JSON) and os.path.getsize(OUT_JSON) > 0:
    with open(OUT_JSON, "r") as f:
        results = json.load(f)

processed = {r["filing_path"] for r in results}

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

for path in filepaths:
    if path in processed:
        continue

    with open(path, "r", encoding="utf-8", errors="replace") as f:
        filing_text = f.read()

    resp = client.responses.parse(
        model="gpt-4.1-nano",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": filing_text},
        ],
        text_format=Form3Filing,
    )

    parsed = resp.output_parsed.model_dump()
    parsed["filing_path"] = path

    results.append(parsed)
    # -------- Save results after each file is processed --------
    with open(OUT_JSON, "w") as out_f:
        json.dump(results, out_f, indent=2)

print(f"[done] Saved {len(results)} records to {OUT_JSON}")

