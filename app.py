import subprocess, sys

subprocess.run([
    sys.executable, "-m", "pip", "install",
    "streamlit",
    "sarvamai",
    "groq",
    "audio-recorder-streamlit",
    "pydub",
    "requests"
], check=True)
import streamlit as st
from audio_recorder_streamlit import audio_recorder
import tempfile, os

#2. fix path
base = "/Workspace/Users/24b0046@iitb.ac.in/KisaanVaani"
sys.path.insert(0, base)
sys.path.insert(0, f"{base}/pipeline")  # Add pipeline dir so 'data' module is discoverable



# ── Pipeline imports ──────────────────────────────────────────────────────────
from pipeline.transcribe import transcribe, from_text
from pipeline.translate  import to_english, to_indic
from pipeline.intent     import extract_intent
from pipeline.Router     import route
from pipeline.answer     import generate_answer

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="KisaanVaani",
    page_icon="🌾",
    layout="centered",
)

st.title("🌾 KisaanVaani")
st.caption("किसान की आवाज़ — Farmer's Voice Assistant")

# ── Language selector ─────────────────────────────────────────────────────────
lang_options = {
    "हिंदी (Hindi)"     : "hi-IN",
    "मराठी (Marathi)"   : "mr-IN",
    "ਪੰਜਾਬੀ (Punjabi)"  : "pa-IN",
    "English"            : "en-IN",
}
selected_lang_label = st.selectbox(
    "अपनी भाषा चुनें / Select your language",
    list(lang_options.keys()),
)
language_code = lang_options[selected_lang_label]

st.divider()

# ── Input mode tabs ───────────────────────────────────────────────────────────
tab_voice, tab_text = st.tabs(["🎤 Voice", "⌨️ Type"])

transcription_result = None   # will be set by whichever tab runs

with tab_voice:
    st.markdown("Click the mic, ask your question, click again to stop.")
    audio_bytes = audio_recorder(
        pause_threshold=3.0,
        text="",
        recording_color="#e74c3c",
        neutral_color="#2ecc71",
        icon_size="2x",
    )

    if audio_bytes:
        st.audio(audio_bytes, format="audio/wav")
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        try:
            transcription_result = transcribe(tmp_path)
        finally:
            os.unlink(tmp_path)

        st.success(f"Heard: **{transcription_result['text']}**  \n"
                   f"Language: {transcription_result['language_name']}")

with tab_text:
    typed_text = st.text_area(
        "अपना सवाल यहाँ लिखें / Type your question here",
        placeholder="e.g. नाशिक में प्याज का भाव क्या है?",
        height=100,
    )
    if st.button("Ask", type="primary", use_container_width=True):
        if typed_text.strip():
            transcription_result = from_text(typed_text.strip(), language_code)
        else:
            st.warning("Please type a question first.")

# ── Pipeline runner ───────────────────────────────────────────────────────────
def run_pipeline(transcription: dict) -> dict:
    """
    Runs the full KisaanVaani pipeline.
    Returns the answer dict from answer.py.
    """
    lang_code = transcription["language_code"]
    raw_text  = transcription["text"]

    with st.status("Processing your question…", expanded=True) as status:

        # Step 1 — translate to English
        st.write("Translating to English…")
        english_text = to_english(raw_text, lang_code)

        # Step 2 — extract intent
        st.write("Understanding your question…")
        intent = extract_intent(english_text)

        # Step 3 — route to data source
        st.write(f"Fetching {intent.get('question_type', 'advisory')} data…")
        data = route(intent)

        # Step 4 — generate answer
        st.write("Generating answer…")
        answer = generate_answer(intent, data, lang_code)

        status.update(label="Done!", state="complete", expanded=False)

    return answer


# ── Run pipeline when we have a transcription ─────────────────────────────────
if transcription_result:
    answer = run_pipeline(transcription_result)

    st.divider()

    # ── Answer display ────────────────────────────────────────────────────────
    lang_name = transcription_result["language_name"]
    local_ans = answer.get("answer_local") or answer.get("answer_english", "")
    eng_ans   = answer.get("answer_english", "")

    st.subheader("Answer")

    # Primary answer — in farmer's language
    st.info(local_ans)

    # English translation (expandable)
    with st.expander("English translation"):
        st.write(eng_ans)

    # Debug info (expandable — useful during development)
    with st.expander("Pipeline details (debug)"):
        intent_keys = ["question_type", "crop", "location", "situation"]
        for k in intent_keys:
            v = answer.get(k) or transcription_result.get(k)
            if v:
                st.write(f"**{k.replace('_', ' ').title()}:** {v}")

    st.divider()
    st.caption("Data sources: data.gov.in · open-meteo.com · Sarvam AI · Groq")