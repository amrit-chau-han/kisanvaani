from groq import Groq

try:
    groq_api_key = dbutils.secrets.get(scope="kisanvaani", key="groq_api_key")
except:
    groq_api_key = "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"  # local fallback

client = Groq(api_key=groq_api_key)

# ── Static agri knowledge base ────────────────────────────────────────────────
# In production this will be a FAISS vector index over agri extension docs
# For now the LLM uses this as grounding context

ADVISORY_CONTEXT = """
WHEAT:
- Sowing: October-November (Rabi season)
- Harvest: March-April
- Common pests: aphids, rust fungus, armyworm
- Fertilizer: NPK 120:60:40 kg/ha, apply urea in 2 splits
- Water: 4-6 irrigations, critical at crown root stage

PADDY / RICE:
- Sowing: June-July (Kharif season)
- Harvest: October-November
- Common pests: brown planthopper, stem borer, blast disease
- Fertilizer: NPK 100:50:50 kg/ha
- Water: keep 5cm standing water during tillering

ONION:
- Sowing: October-November (Rabi), June-July (Kharif)
- Harvest: 90-120 days after transplanting
- Common issues: purple blotch, thrips, basal rot
- Fertilizer: NPK 100:50:50 kg/ha + sulphur 20kg/ha
- Water: light and frequent, avoid waterlogging

TOMATO:
- Sowing: June-July and October-November
- Harvest: 60-80 days after transplanting
- Common pests: fruit borer, leaf curl virus, early blight
- Fertilizer: NPK 100:60:80 kg/ha
- Water: drip irrigation preferred, 600-800mm total

COTTON:
- Sowing: April-May (Maharashtra), May-June (Punjab)
- Harvest: October-November
- Common pests: bollworm, whitefly, mealybug
- Fertilizer: NPK 120:60:60 kg/ha
- Water: critical at flowering and boll development stages

SUGARCANE:
- Sowing: February-March
- Harvest: 12-18 months after planting
- Common pests: internode borer, woolly aphid, red rot
- Fertilizer: NPK 250:85:85 kg/ha applied in splits
- Water: high water need, 1500-2500mm

GENERAL PEST CONTROL:
- Neem-based pesticides are safe and effective for most pests
- Never spray pesticides during flowering — kills pollinators
- Rotate pesticide groups to prevent resistance
- Contact your nearest KVK for free soil testing
"""


def get_advisory(crop, situation):
    """
    Input : crop      = "wheat"
            situation = "yellow leaves on wheat plants"

    Output: {
                "crop"      : "wheat",
                "problem"   : "yellow leaves",
                "cause"     : "likely nitrogen deficiency or rust fungus",
                "solution"  : "apply urea top dressing, check for rust spots",
                "prevention": "balanced fertilizer application next season",
                "answer"    : "Full plain-language advice for the farmer..."
            }
    """

    prompt = f"""You are an expert agricultural advisor for Indian farmers.
Use the information below to give practical advice.

AGRICULTURAL KNOWLEDGE BASE:
{ADVISORY_CONTEXT}

Crop     : {crop if crop else "not specified"}
Situation: {situation}

Return ONLY a JSON object in exactly this format:
{{
    "crop"       : "crop name",
    "problem"    : "identified problem in one line",
    "cause"      : "most likely cause",
    "solution"   : "immediate action the farmer should take",
    "prevention" : "how to prevent this in future",
    "answer"     : "2-3 sentence practical advice in simple language"
}}"""

    print(f"Advisory     : fetching advice for {crop} — {situation}")

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

    print(f"Advisory     : problem identified = {result.get('problem')}")
    return result


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — pest problem
    r1 = get_advisory("tomato", "fruit borer attack on tomato plants")
    print(f"\n{r1}\n")

    # Test 2 — sowing advice
    r2 = get_advisory("cotton", "when should I sow cotton in Maharashtra")
    print(f"\n{r2}\n")

    # Test 3 — no crop specified
    r3 = get_advisory(None, "yellow leaves on my plants")
    print(f"\n{r3}\n")
