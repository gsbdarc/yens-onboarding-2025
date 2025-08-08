import os
import sys
import json
import pandas as pd
from typing import List
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

CSV_PATH = "/scratch/shared/yens-onboarding-2025/data/form_3_100.csv"
ENV_PATH = "/scratch/shared/yens-onboarding-2025/.env"

class Form3Filing(BaseModel):
    insider_name: str
    insider_role: List[str]
    company_name: str
    company_cik: str
    filing_date: str

# Get index from first CLI argument
if len(sys.argv) < 2:
    raise ValueError("Usage: python extract_form_3_one_from_csv.py <index>")
idx = int(sys.argv[1])

# Load secrets & OpenAI client
load_dotenv(ENV_PATH)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Read filepath from CSV
df = pd.read_csv(CSV_PATH)
filing_path = df.loc[idx, "filepath"]

with open(filing_path, "r", encoding="utf-8", errors="replace") as f:
    filing_text = f.read()

system_prompt = """
You are a data extraction agent for SEC Form 3 filings.

Extract:
- insider_name
- insider_role (list)
- company_name
- company_cik
- filing_date

Return valid JSON matching the provided Pydantic model.
"""
resp = client.responses.parse(
    model="gpt-4.1-nano",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": filing_text}
    ],
    text_format=Form3Filing,
)

parsed = resp.output_parsed.model_dump()
parsed["filing_path"] = filing_path
parsed["row_index"] = idx

# Save one JSON per task
os.makedirs("results/array", exist_ok=True)
out_file = f"results/array/form3_row_{idx}.json"
with open(out_file, "w") as out_f:
    json.dump(parsed, out_f, indent=2)

print(f"[done] {out_file}")
