from groq import Groq

try:
    groq_api_key = dbutils.secrets.get(scope="kisanvaani", key="groq_api_key")
except:
    groq_api_key = "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"  # local fallback

client = Groq(api_key=groq_api_key)

# ── Static knowledge base of major Indian farming schemes ────────────────────
# In production this will be replaced by a proper RAG / vector search
# For now the LLM uses this as grounding context

SCHEMES_CONTEXT = """
PM-KISAN (Pradhan Mantri Kisan Samman Nidhi):
- ₹6000/year direct benefit in 3 instalments of ₹2000
- For all landholding farmer families
- Apply at pmkisan.gov.in or nearest CSC centre
- Documents: Aadhaar, bank account, land records

PM Fasal Bima Yojana (Crop Insurance):
- Subsidised crop insurance for Kharif and Rabi crops
- Premium: 2% for Kharif, 1.5% for Rabi, 5% for horticulture
- Apply through bank or insurance company before sowing
- Documents: land records, bank account, Aadhaar

Kisan Credit Card (KCC):
- Low interest crop loan (4% after subvention)
- Up to ₹3 lakh without collateral
- Apply at any nationalised bank or cooperative bank
- Documents: land records, Aadhaar, passport photo

PM Krishi Sinchayee Yojana (Irrigation):
- Subsidy for drip and sprinkler irrigation
- Up to 55% subsidy for small/marginal farmers
- Apply through state agriculture department
- Documents: land records, Aadhaar, bank account

eNAM (National Agriculture Market):
- Online mandi platform for better price discovery
- Register at enam.gov.in
- Documents: Aadhaar, bank account, mandi license

Soil Health Card Scheme:
- Free soil testing and health card every 2 years
- Fertilizer recommendations specific to your field
- Contact nearest Krishi Vigyan Kendra (KVK)
"""


def get_scheme_info(situation):
    """
    Input : situation = "PM Kisan application help"

    Output: {
                "scheme_name" : "PM-KISAN",
                "benefit"     : "₹6000/year in 3 instalments",
                "eligibility" : "All landholding farmer families",
                "how_to_apply": "pmkisan.gov.in or nearest CSC centre",
                "documents"   : "Aadhaar, bank account, land records",
                "answer"      : "Full plain-language explanation..."
            }
    """

    prompt = f"""You are a helpful assistant for Indian farmers.
A farmer wants to know about government schemes.
Use the information below to answer their question.

SCHEMES INFORMATION:
{SCHEMES_CONTEXT}

Farmer's situation: "{situation}"

Return ONLY a JSON object in exactly this format:
{{
    "scheme_name"  : "name of the most relevant scheme",
    "benefit"      : "main financial benefit in one line",
    "eligibility"  : "who can apply",
    "how_to_apply" : "where and how to apply",
    "documents"    : "documents needed",
    "answer"       : "2-3 sentence plain explanation for the farmer"
}}"""

    print(f"Schemes      : looking up scheme for — {situation}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role"   : "user",
                "content": prompt
            }
        ],
        temperature=0.0
    )

    raw = response.choices[0].message.content.strip()

    # extract JSON
    start    = raw.find("{")
    end      = raw.rfind("}") + 1
    json_str = raw[start:end]

    import json
    result = json.loads(json_str)

    print(f"Schemes      : matched scheme = {result.get('scheme_name')}")
    return result


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — PM Kisan
    r1 = get_scheme_info("How do I apply for PM Kisan scheme?")
    print(f"\n{r1}\n")

    # Test 2 — crop insurance
    r2 = get_scheme_info("I want to insure my wheat crop")
    print(f"\n{r2}\n")

    # Test 3 — loan
    r3 = get_scheme_info("I need a low interest loan for farming")
    print(f"\n{r3}\n")
from groq import Groq

try:
    groq_api_key = dbutils.secrets.get(scope="kisanvaani", key="groq_api_key")
except:
    groq_api_key = "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"  # local fallback

client = Groq(api_key=groq_api_key)

# ── Static knowledge base of major Indian farming schemes ────────────────────
# In production this will be replaced by a proper RAG / vector search
# For now the LLM uses this as grounding context

SCHEMES_CONTEXT = """
PM-KISAN (Pradhan Mantri Kisan Samman Nidhi):
- ₹6000/year direct benefit in 3 instalments of ₹2000
- For all landholding farmer families
- Apply at pmkisan.gov.in or nearest CSC centre
- Documents: Aadhaar, bank account, land records

PM Fasal Bima Yojana (Crop Insurance):
- Subsidised crop insurance for Kharif and Rabi crops
- Premium: 2% for Kharif, 1.5% for Rabi, 5% for horticulture
- Apply through bank or insurance company before sowing
- Documents: land records, bank account, Aadhaar

Kisan Credit Card (KCC):
- Low interest crop loan (4% after subvention)
- Up to ₹3 lakh without collateral
- Apply at any nationalised bank or cooperative bank
- Documents: land records, Aadhaar, passport photo

PM Krishi Sinchayee Yojana (Irrigation):
- Subsidy for drip and sprinkler irrigation
- Up to 55% subsidy for small/marginal farmers
- Apply through state agriculture department
- Documents: land records, Aadhaar, bank account

eNAM (National Agriculture Market):
- Online mandi platform for better price discovery
- Register at enam.gov.in
- Documents: Aadhaar, bank account, mandi license

Soil Health Card Scheme:
- Free soil testing and health card every 2 years
- Fertilizer recommendations specific to your field
- Contact nearest Krishi Vigyan Kendra (KVK)
"""


def get_scheme_info(situation):
    """
    Input : situation = "PM Kisan application help"

    Output: {
                "scheme_name" : "PM-KISAN",
                "benefit"     : "₹6000/year in 3 instalments",
                "eligibility" : "All landholding farmer families",
                "how_to_apply": "pmkisan.gov.in or nearest CSC centre",
                "documents"   : "Aadhaar, bank account, land records",
                "answer"      : "Full plain-language explanation..."
            }
    """

    prompt = f"""You are a helpful assistant for Indian farmers.
A farmer wants to know about government schemes.
Use the information below to answer their question.

SCHEMES INFORMATION:
{SCHEMES_CONTEXT}

Farmer's situation: "{situation}"

Return ONLY a JSON object in exactly this format:
{{
    "scheme_name"  : "name of the most relevant scheme",
    "benefit"      : "main financial benefit in one line",
    "eligibility"  : "who can apply",
    "how_to_apply" : "where and how to apply",
    "documents"    : "documents needed",
    "answer"       : "2-3 sentence plain explanation for the farmer"
}}"""

    print(f"Schemes      : looking up scheme for — {situation}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role"   : "user",
                "content": prompt
            }
        ],
        temperature=0.0
    )

    raw = response.choices[0].message.content.strip()

    # extract JSON
    start    = raw.find("{")
    end      = raw.rfind("}") + 1
    json_str = raw[start:end]

    import json
    result = json.loads(json_str)

    print(f"Schemes      : matched scheme = {result.get('scheme_name')}")
    return result


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — PM Kisan
    r1 = get_scheme_info("How do I apply for PM Kisan scheme?")
    print(f"\n{r1}\n")

    # Test 2 — crop insurance
    r2 = get_scheme_info("I want to insure my wheat crop")
    print(f"\n{r2}\n")

    # Test 3 — loan
    r3 = get_scheme_info("I need a low interest loan for farming")
    print(f"\n{r3}\n")
