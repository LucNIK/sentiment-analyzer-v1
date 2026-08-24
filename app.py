# Author: NIKABOU NADJOMBE
# Date: 2025-09-24

import time
from datetime import datetime

import streamlit as st
from transformers import pipeline


# ----------- CONFIG STREAMLIT -----------
st.set_page_config(
    page_title="🧠 Sentiment Analyzer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ----------- SENTIMENT HELPERS -----------
def get_sentiment_style(label):
    """Return the emoji and color associated with a sentiment label."""
    styles = {
        "POSITIVE": {
            "emoji": "😄",
            "color": "#4CAF50"
        },
        "NEGATIVE": {
            "emoji": "😢",
            "color": "#FF4B4B"
        },
        "NEUTRAL": {
            "emoji": "😐",
            "color": "#FFA500"
        }
    }

    return styles.get(
        label,
        {
            "emoji": "💭",
            "color": "#808080"
        }
    )


# ----------- HISTORIQUE DES DISCUSSIONS -----------
if "history" not in st.session_state:
    st.session_state.history = []


# ----------- PIPELINE HUGGING FACE -----------
@st.cache_resource
def load_classifier():
    """Load and cache the sentiment analysis pipeline."""
    return pipeline("sentiment-analysis")


classifier = load_classifier()


# ----------- INTERFACE PRINCIPALE -----------
st.title("🧠 Sentiment Analyzer")
st.write("Enter a sentence to analyze its sentiment:")

with st.form("sentiment_form", clear_on_submit=True):
    user_input = st.text_input("Your text:")
    submitted = st.form_submit_button("Analyze")


# ----------- ANALYSE DU SENTIMENT -----------
if submitted:
    user_input = user_input.strip()

    if not user_input:
        st.warning("Please enter some text before analyzing.")
    else:
        try:
            # ----------- ANIMATION DE PROGRESSION -----------
            progress_bar = st.progress(0)
            status_text = st.empty()

            for percent in range(0, 101, 10):
                time.sleep(0.05)
                progress_bar.progress(percent)
                status_text.text(f"Analyzing... {percent}%")

            progress_bar.empty()
            status_text.empty()

            # ----------- ANALYSE -----------
            result = classifier(user_input)[0]

            label = result["label"].upper()
            score = result["score"]

            # ----------- STYLE DU SENTIMENT -----------
            sentiment_style = get_sentiment_style(label)
            emoji = sentiment_style["emoji"]
            color = sentiment_style["color"]

            # ----------- RESULTAT -----------
            st.markdown(
                f"<h2 style='color:{color}; font-size:2rem'>"
                f"{emoji} {label}"
                f"</h2>",
                unsafe_allow_html=True
            )

            st.progress(score)

            st.markdown(
                f"**Confidence:** {score * 100:.1f}%"
            )

            # ----------- AJOUT A L'HISTORIQUE -----------
            st.session_state.history.append(
                {
                    "text": user_input,
                    "label": label,
                    "score": score,
                    "time": datetime.now().strftime("%H:%M:%S")
                }
            )

        except Exception as error:
            st.error(
                "An error occurred while analyzing the text. "
                "Please try again."
            )
            st.caption(f"Error details: {error}")


# ----------- SIDEBAR HISTORIQUE -----------
st.sidebar.title("📜 History")

if st.session_state.history:
    for item in reversed(st.session_state.history):

        # Determine the color for EACH history item independently.
        item_style = get_sentiment_style(item["label"])

        item_color = item_style["color"]
        item_emoji = item_style["emoji"]

        st.sidebar.markdown(
            f"<p style='color:{item_color}; margin:0'>"
            f"{item_emoji} {item['time']} | "
            f"{item['label']} "
            f"({item['score'] * 100:.1f}%)"
            f"</p>"
            f"<p style='margin-left:10px'>"
            f"{item['text']}"
            f"</p>"
            "<hr style='border:1px solid #ccc'>",
            unsafe_allow_html=True
        )
else:
    st.sidebar.write(
        "No history yet. Submit a sentence to see it here."
    )


# ----------- STYLING STREAMLIT MODERNE -----------
st.markdown(
    """
    <style>
        .stTextInput>div>div>input {
            height: 2.8rem;
            font-size: 1.1rem;
            padding-left: 10px;
            border-radius: 10px;
        }

        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 1.1rem;
            padding: 10px 20px;
            border-radius: 8px;
            transition: 0.3s;
        }

        .stButton>button:hover {
            background-color: #45a049;
            cursor: pointer;
        }

        .stProgress>div>div>div>div {
            background-color: #4CAF50;
        }

        .css-18e3th9 {
            padding-top: 2rem;
        }

        .css-1d391kg {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)
