#Author: NIKABOU NADJOMBE
#Date: 2025-09-24

import streamlit as st
from transformers import pipeline
from datetime import datetime
import time

# ----------- CONFIG STREAMLIT -----------
st.set_page_config(
    page_title="🧠 Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------- HISTORIQUE DES DISCUSSIONS -----------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------- PIPELINE HUGGINGFACE -----------
classifier = pipeline("sentiment-analysis")

# ----------- INTERFACE PRINCIPALE -----------
st.title("🧠 Sentiment Analyzer")
st.write("Enter a sentence to analyze its sentiment:")

with st.form("sentiment_form", clear_on_submit=True):
    user_input = st.text_input("Your text:")
    submitted = st.form_submit_button("Analyze")

if submitted and user_input:
    # ----------- ANIMATION DE PROGRESSION -----------
    progress_bar = st.progress(0)
    status_text = st.empty()
    for percent in range(0, 101, 10):
        time.sleep(0.05)
        progress_bar.progress(percent)
        status_text.text(f"Analyzing... {percent}%")
    progress_bar.empty()
    status_text.empty()

    # ----------- ANALYSE DU SENTIMENT -----------
    result = classifier(user_input)[0]
    label = result["label"]
    score = result["score"]

    # Emoji selon le sentiment
    emoji = "😄" if label == "POSITIVE" else "😢" if label == "NEGATIVE" else "😐"

    # Couleur personnalisée pour le label
    color = "#4CAF50" if label == "POSITIVE" else "#FF4B4B" if label == "NEGATIVE" else "#FFA500"

    st.markdown(f"<h2 style='color:{color}; font-size:2rem'>{emoji} {label}</h2>", unsafe_allow_html=True)

    # Barre de score colorée
    st.progress(score)  # Streamlit standard progress bar
    st.markdown(f"**Confidence:** {score*100:.1f}%")

    # Ajout à l'historique
    st.session_state.history.append({
        "text": user_input,
        "label": label,
        "score": score,
        "time": datetime.now().strftime("%H:%M:%S")
    })

# ----------- SIDEBAR HISTORIQUE -----------
st.sidebar.title("📜 History")
if st.session_state.history:
    for item in reversed(st.session_state.history):
        st.sidebar.markdown(
            f"<p style='color:{color}; margin:0'>{item['time']} | {item['label']} ({item['score']*100:.1f}%)</p>"
            f"<p style='margin-left:10px'>{item['text']}</p>"
            "<hr style='border:1px solid #ccc'>",
            unsafe_allow_html=True
        )
else:
    st.sidebar.write("No history yet. Submit a sentence to see it here.")

# ----------- STYLING STREAMLIT MODERNE -----------
st.markdown("""
<style>
    .stTextInput>div>div>input {height: 2.8rem; font-size: 1.1rem; padding-left:10px; border-radius:10px;}
    .stButton>button {background-color: #4CAF50; color: white; font-size: 1.1rem; padding:10px 20px; border-radius:8px; transition: 0.3s;}
    .stButton>button:hover {background-color: #45a049; cursor: pointer;}
    .stProgress>div>div>div>div {background-color: #4CAF50;} /* couleur progressbar */
    .css-18e3th9 {padding-top: 2rem;}
    .css-1d391kg {padding-top: 1rem;}
</style>
""", unsafe_allow_html=True)
