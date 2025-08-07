import os
from openai import OpenAI
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv

# Path to your filing
filing_path = "/zfs/data/NODR/EDGAR_HTTPS/edgar/data/1656998/0000950103-24-000077"

with open(filing_path, "r") as f:
    filing_text = f.read()

# Load environment variables
load_dotenv('/scratch/shared/yens-onboarding-2025/.env')
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define your Pydantic model for GPT response
class Form3Filing(BaseModel):
    insider_name: str
    insider_role: List[str]
    company_name: str
    company_cik: str
    filing_date: str

# Prompts
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

user_prompt = filing_text

# Call OpenAI
response = client.responses.parse(
    model="gpt-4.1-nano",
    input=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    text_format=Form3Filing,
)

output_parsed = response.output_parsed

print(output_parsed.model_dump())
