# Databricks notebook source
# MAGIC %pip install groq sarvamai streamlit audio-recorder-streamlit pydub requests
# MAGIC

# COMMAND ----------

dbutils.library.restartPython()

# COMMAND ----------

import sys, os

base = "/Workspace/Users/your-email@domain.com/KisaanVaani"
sys.path.insert(0, base)

tests = [
    ("groq",                          "from groq import Groq"),
    ("sarvamai",                      "from sarvamai import SarvamAI"),
    ("streamlit",                     "import streamlit as st"),
    ("audio_recorder_streamlit",      "from audio_recorder_streamlit import audio_recorder"),
    ("pipeline.transcribe",           "from pipeline.transcribe import from_text"),
    ("pipeline.translate",            "from pipeline.translate import to_english"),
    ("pipeline.intent",               "from pipeline.intent import extract_intent"),
    ("pipeline.Router",               "from pipeline.Router import route"),
    ("pipeline.answer",               "from pipeline.answer import generate_answer"),
    ("pipeline.data.Mandi",           "from pipeline.data.Mandi import get_mandi_price"),
    ("pipeline.data.weather",         "from pipeline.data.weather import get_weather"),
    ("pipeline.data.schemes",         "from pipeline.data.schemes import get_scheme_info"),
    ("pipeline.data.advisory",        "from pipeline.data.advisory import get_advisory"),
]

for name, statement in tests:
    try:
        exec(statement)
        print(f"✅ {name}")
    except Exception as e:
        print(f"❌ {name}: {e}")