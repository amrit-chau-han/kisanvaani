from sarvamai import SarvamAI

client = SarvamAI(api_subscription_key="sk_q9fzyf3w_pQFeAdvzYOvusapEcsZkT2tj")

lang_map = {
    "hi-IN": "Hindi",
    "mr-IN": "Marathi",
    "pa-IN": "Punjabi",
    "en-IN": "English"
}

def transcribe(audio_path):
    """
    Voice input → text + language
    """
    with open(audio_path, "rb") as f:
        response = client.speech_to_text.transcribe(
            file=("audio.wav", f, "audio/wav"),
            model="saarika:v2.5",
            language_code="unknown"
        )

    result = {
        "text": response.transcript,
        "language_code": response.language_code,
        "language_name": lang_map.get(
            response.language_code,
            response.language_code
        )
    }

    print(f"Transcribed : {result['text']}")
    print(f"Language    : {result['language_name']}")
    return result


def from_text(text, language_code="hi-IN"):
    """
    Text input → same dictionary format as transcribe()
    So rest of pipeline works identically for both
    """
    result = {
        "text": text,
        "language_code": language_code,
        "language_name": lang_map.get(language_code, language_code)
    }

    print(f"Text input  : {result['text']}")
    print(f"Language    : {result['language_name']}")
    return result