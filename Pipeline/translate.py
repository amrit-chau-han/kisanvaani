from sarvamai import SarvamAI

client = SarvamAI(api_subscription_key="sk_q9fzyf3w_pQFeAdvzYOvusapEcsZkT2tj")

lang_code_map = {
    "hi-IN": "hi-IN",
    "mr-IN": "mr-IN",
    "pa-IN": "pa-IN",
    "en-IN": "en-IN"
}

def to_english(text, language_code):
    if language_code == "en-IN":
        return text

    response = client.text.translate(
        input=text,
        source_language_code=language_code,  # ← use directly, e.g. "hi-IN"
        target_language_code="en-IN",         # ← en-IN not "en"
        speaker_gender="Male",
        mode="formal",
        model="mayura:v1"
    )

    english = response.translated_text
    print(f"Original : {text}")
    print(f"English  : {english}")
    return english


def to_indic(text, language_code):
    if language_code == "en-IN":
        return text

    response = client.text.translate(
        input=text,
        source_language_code="en-IN",   # ← en-IN not "en"
        target_language_code=language_code,
        speaker_gender="Male",
        mode="formal",
        model="mayura:v1"
    )

    indic = response.translated_text
    print(f"English   : {text}")
    print(f"Translated: {indic}")
    return indic


# ── Test ─────────────────────────────────────────
if __name__ == "__main__":
    # Test Hindi → English
    english = to_english(
        "नाशिक में प्याज का भाव क्या है",
        "hi-IN"
    )
    print(f"\nFor RAG: {english}")

    # Test English → Hindi
    hindi = to_indic(
        "Onion price in Nashik is ₹1200 per quintal",
        "hi-IN"
    )
    print(f"\nFarmer gets: {hindi}")