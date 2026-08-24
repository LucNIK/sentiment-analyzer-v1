# Author: NIKABOU NADJOMBE
# Date: 2025-09-24

import time
from datetime import datetime

import streamlit as st
from transformers import pipeline


# ----------- CONFIGURATION -----------
st.set_page_config(
    page_title="🧠 Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------- SENTIMENT STYLES -----------
def get_sentiment_style(label):
    styles = {
        "POSITIVE": {
            "emoji": "😄",
            "color": "#4CAF50",
            "message": "This text has a positive sentiment."
        },
        "NEGATIVE": {
            "emoji": "😢",
            "color": "#FF4B4B",
            "message": "This text has a negative sentiment."
        },
        "NEUTRAL": {
            "emoji": "😐",
            "color": "#FFA500",
            "message": "This text has a neutral sentiment."
        }
    }

    return styles.get(
        label,
        {
            "emoji": "💭",
            "color": "#808080",
            "message": "Sentiment could not be determined."
        }
    )


# ----------- SESSION STATE -----------
if "history" not in st.session_state:
    st.session_state.history = []

if "statistics_reset_at" not in st.session_state:
    st.session_state.statistics_reset_at = None


# ----------- CLASSIFIER -----------
@st.cache_resource
def load_classifier():
    return pipeline("sentiment-analysis")


classifier = load_classifier()


# ----------- MAIN INTERFACE -----------
st.title("🧠 Sentiment Analyzer")
st.write("Enter a sentence to analyze its sentiment:")

with st.form("sentiment_form", clear_on_submit=True):
    user_input = st.text_input("Your text:")

    # Text statistics
    character_count = len(user_input)
    word_count = len(user_input.split())

    st.caption(
        f"Characters: {character_count} | "
        f"Words: {word_count}"
    )

    submitted = st.form_submit_button("Analyze")


# ----------- ANALYSIS -----------
if submitted:
    user_input = user_input.strip()

    if not user_input:
