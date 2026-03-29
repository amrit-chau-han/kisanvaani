import json
from groq import Groq

client = Groq(api_key="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")

def extract_intent(english_text):
    """
    Input  : English text from translate.py
    Output : {
                "crop": "onion",
                "location": "Nashik",
                "situation": "price inquiry",
                "question_type": "price/weather/scheme/advisory"
             }
    """

    prompt = f"""
You are an AI assistant that extracts farming information.
Extract information from the farmer's question and return ONLY a JSON object.
No explanation, no extra text, just the JSON.

question_type must be ONE of: "price", "weather", "scheme", "advisory"

Rules:
- price    → farmer asking about crop prices or mandi rates
- weather  → farmer asking about rain, temperature, forecast
- scheme   → farmer asking about government schemes or subsidies
- advisory → farmer asking about farming advice, pest control, sowing

If any field is not mentioned, use null.

Farmer question: "{english_text}"

Return exactly this format:
{{
    "crop": "crop name or null",
    "location": "city or district or null",
    "situation": "one line description",
    "question_type": "price/weather/scheme/advisory"
}}
"""

    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",   # ← current recommended model
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.0
)

    raw = response.choices[0].message.content.strip()

    # Clean up response in case LLM adds extra text
    # Find JSON part
    start = raw.find("{")
    end = raw.rfind("}") + 1
    json_str = raw[start:end]

    result = json.loads(json_str)

    print(f"Question     : {english_text}")
    print(f"Crop         : {result.get('crop')}")
    print(f"Location     : {result.get('location')}")
    print(f"Situation    : {result.get('situation')}")
    print(f"Question Type: {result.get('question_type')}")

    return result


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — price question
    r1 = extract_intent("What is the price of onion in Nashik today?")
    print(f"\n{r1}\n")

    # Test 2 — weather question
    r2 = extract_intent("Will it rain in Pune this week?")
    print(f"\n{r2}\n")

    # Test 3 — scheme question
    r3 = extract_intent("How do I apply for PM Kisan scheme?")
    print(f"\n{r3}\n")

    # Test 4 — advisory question
    r4 = extract_intent("When should I sow cotton in Maharashtra?")
    print(f"\n{r4}\n")
