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
    """Return the emoji, color and message for a sentiment."""
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


# ----------- HISTORIQUE -----------
if "history" not in st.session_state:
    st.session_state.history = []


# ----------- HUGGING FACE PIPELINE -----------
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


# ----------- ANALYSE -----------
if submitted:
    user_input = user_input.strip()

    if not user_input:
        st.warning("Please enter some text before analyzing.")
    else:
        try:
            # ----------- PROGRESSION -----------
            progress_bar = st.progress(0)
            status_text = st.empty()

            for percent in range(0, 101, 10):
                time.sleep(0.05)
                progress_bar.progress(percent)
                status_text.text(f"Analyzing... {percent}%")

            progress_bar.empty()
            status_text.empty()

            # ----------- SENTIMENT -----------
            result = classifier(user_input)[0]

            label = result["label"].upper()
            score = result["score"]

            # ----------- STYLE -----------
            sentiment = get_sentiment_style(label)

            emoji = sentiment["emoji"]
            color = sentiment["color"]
            message = sentiment["message"]

            # ----------- RESULTAT -----------
            st.markdown(
                f"""
                <div style="
                    padding: 20px;
                    border-radius: 12px;
                    border-left: 6px solid {color};
                    background-color: rgba(128,128,128,0.08);
                ">
                    <h2 style="color:{color}; margin-bottom:5px;">
                        {emoji} {label}
                    </h2>
                    <p style="font-size:1.1rem; margin:0;">
                        {message}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Confidence")
            st.progress(score)
            st.markdown(f"**{score * 100:.1f}%**")

            # ----------- HISTORIQUE -----------
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

        item_style = get_sentiment_style(item["label"])

        st.sidebar.markdown(
            f"""
            <p style="color:{item_style['color']}; margin:0;">
                {item_style['emoji']} {item['time']} |
                {item['label']} ({item['score'] * 100:.1f}%)
            </p>
            <p style="margin-left:10px;">
                {item['text']}
            </p>
            <hr style="border:1px solid #ccc;">
            """,
            unsafe_allow_html=True
        )
else:
    st.sidebar.write(
        "No history yet. Submit a sentence to see it here."
    )


# ----------- STYLING -----------
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
