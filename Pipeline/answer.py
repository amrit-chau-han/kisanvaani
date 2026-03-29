from groq import Groq

try:
    groq_api_key = dbutils.secrets.get(scope="kisanvaani", key="groq_api_key")
except:
    groq_api_key = "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"  # local fallback

client = Groq(api_key=groq_api_key)


def generate_answer(intent, data, language_code):
    """
    Input : intent        = { "crop": "onion", "location": "Nashik", ... }
            data          = raw dict from mandi.py / weather.py / schemes.py / advisory.py
            language_code = "hi-IN" / "mr-IN" / "pa-IN" / "en-IN"

    Output: {
                "answer_english" : "The price of onion in Nashik is ₹1200 per quintal.",
                "answer_hindi"   : "नासिक में प्याज का भाव ₹1200 प्रति क्विंटल है।",
                "language_code"  : "hi-IN"
            }

    Note: translation to farmer's language happens here using the LLM directly.
          For production use translate.py (Sarvam) for better Indic quality.
    """

    question_type = intent.get("question_type", "advisory")
    crop          = intent.get("crop")
    location      = intent.get("location")
    situation     = intent.get("situation")

    # Build context string from data dict
    data_context = "\n".join([f"{k}: {v}" for k, v in data.items()])

    # Map language code to language name for the prompt
    language_names = {
        "hi-IN" : "Hindi",
        "mr-IN" : "Marathi",
        "pa-IN" : "Punjabi",
        "en-IN" : "English",
        "te-IN" : "Telugu",
        "kn-IN" : "Kannada",
        "ta-IN" : "Tamil",
        "gu-IN" : "Gujarati",
    }
    language_name = language_names.get(language_code, "Hindi")

    prompt = f"""You are KisanVaani, a helpful AI assistant for Indian farmers.
Generate a clear, friendly answer for the farmer using the data provided.

Farmer's question type : {question_type}
Crop                   : {crop if crop else "not specified"}
Location               : {location if location else "not specified"}
Situation              : {situation}

DATA FROM SOURCE:
{data_context}

Instructions:
- Write a clear, simple answer that directly helps the farmer
- Use specific numbers and facts from the data above
- Keep it short — 2 to 3 sentences max
- Avoid technical jargon — farmer must understand it easily

Return ONLY a JSON object in exactly this format:
{{
    "answer_english" : "your answer in English",
    "answer_local"   : "same answer translated to {language_name}",
    "language_code"  : "{language_code}"
}}"""

    print(f"Answer       : generating for question_type = {question_type}, language = {language_name}")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role"   : "user",
                "content": prompt
            }
        ],
        temperature=0.1
    )

    raw = response.choices[0].message.content.strip()

    # extract JSON
    start    = raw.find("{")
    end      = raw.rfind("}") + 1
    json_str = raw[start:end]

    import json
    result = json.loads(json_str)

    print(f"Answer       : {result.get('answer_english')}")
    return result


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":

    # Test 1 — price answer in Hindi
    r1 = generate_answer(
        intent = {
            "crop"          : "onion",
            "location"      : "Nashik",
            "situation"     : "price inquiry",
            "question_type" : "price"
        },
        data = {
            "crop"     : "onion",
            "location" : "Nashik",
            "price"    : "1200",
            "unit"     : "per quintal",
            "market"   : "Nashik APMC",
            "date"     : "2025-01-15",
            "source"   : "data.gov.in"
        },
        language_code = "hi-IN"
    )
    print(f"\n{r1}\n")

    # Test 2 — weather answer in Marathi
    r2 = generate_answer(
        intent = {
            "crop"          : None,
            "location"      : "Pune",
            "situation"     : "rain forecast",
            "question_type" : "weather"
        },
        data = {
            "location"    : "Pune",
            "temperature" : "28°C",
            "rainfall_mm" : "12.4",
            "humidity"    : "74%",
            "condition"   : "Currently 28°C, humidity 74%",
            "forecast"    : "Light rain expected — 18.2mm over 3 days",
            "source"      : "open-meteo.com"
        },
        language_code = "mr-IN"
    )
    print(f"\n{r2}\n")

    # Test 3 — advisory answer in Punjabi
    r3 = generate_answer(
        intent = {
            "crop"          : "wheat",
            "location"      : "Amritsar",
            "situation"     : "yellow leaves on wheat",
            "question_type" : "advisory"
        },
        data = {
            "crop"       : "wheat",
            "problem"    : "yellow leaves",
            "cause"      : "nitrogen deficiency or rust fungus",
            "solution"   : "apply urea top dressing, check for rust spots",
            "prevention" : "balanced fertilizer next season",
            "answer"     : "Apply urea immediately and inspect for orange rust spots."
        },
        language_code = "pa-IN"
    )
    print(f"\n{r3}\n")
