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
        st.warning("Please enter some text before analyzing.")
    else:
        try:
            progress_bar = st.progress(0)
            status_text = st.empty()

            for percent in range(0, 101, 10):
                time.sleep(0.05)
                progress_bar.progress(percent)
                status_text.text(f"Analyzing... {percent}%")

            progress_bar.empty()
            status_text.empty()

            result = classifier(user_input)[0]

            label = result["label"].upper()
            score = result["score"]

            sentiment = get_sentiment_style(label)

            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:12px;
                    border-left:6px solid {sentiment['color']};
                    background-color:rgba(128,128,128,0.08);
                ">
                    <h2 style="color:{sentiment['color']};">
                        {sentiment['emoji']} {label}
                    </h2>
                    <p>{sentiment['message']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Confidence")
            st.progress(score)
            st.markdown(f"**{score * 100:.1f}%**")

            st.session_state.history.append(
                {
                    "text": user_input,
                    "label": label,
                    "score": score,
                    "time": datetime.now().strftime("%H:%M:%S"),
                    "created_at": datetime.now()
                }
            )

        except Exception as error:
            st.error(
                "An error occurred while analyzing the text. "
                "Please try again."
            )
            st.caption(f"Error details: {error}")


# ----------- SIDEBAR -----------
st.sidebar.title("📜 History")

if st.session_state.statistics_reset_at:
    statistics_history = [
        item
        for item in st.session_state.history
        if item["created_at"] > st.session_state.statistics_reset_at
    ]
else:
    statistics_history = st.session_state.history


analysis_count = len(statistics_history)

positive_count = sum(
    item["label"] == "POSITIVE"
    for item in statistics_history
)

negative_count = sum(
    item["label"] == "NEGATIVE"
    for item in statistics_history
)

neutral_count = sum(
    item["label"] == "NEUTRAL"
    for item in statistics_history
)


# ----------- ANALYSIS COUNTER -----------
st.sidebar.metric(
    "📊 Analyses",
    analysis_count
)


# ----------- SENTIMENT STATISTICS -----------
st.sidebar.markdown("### 📈 Sentiment Statistics")

st.sidebar.markdown(f"😄 **Positive:** {positive_count}")
st.sidebar.markdown(f"😢 **Negative:** {negative_count}")
st.sidebar.markdown(f"😐 **Neutral:** {neutral_count}")


# ----------- RESET STATISTICS -----------
if st.sidebar.button("🔄 Reset Statistics"):
    st.session_state.statistics_reset_at = datetime.now()
    st.rerun()


# ----------- LAST ANALYSIS -----------
if st.session_state.history:
    last_analysis = st.session_state.history[-1]
    last_style = get_sentiment_style(last_analysis["label"])

    last_text = last_analysis["text"]
    last_characters = len(last_text)
    last_words = len(last_text.split())

    st.sidebar.markdown("### 🔎 Last Analysis")

    st.sidebar.markdown(
        f"""
        <div style="
            padding:10px;
            border-left:4px solid {last_style['color']};
            border-radius:6px;
            background-color:rgba(128,128,128,0.08);
        ">
            <strong>
                {last_style['emoji']} {last_analysis['label']}
            </strong>
            <br>
            Confidence: {last_analysis['score'] * 100:.1f}%
            <br>
            Characters: {last_characters}
            <br>
            Words: {last_words}
            <br>
            <small>{last_analysis['time']}</small>
        </div>
        """,
        unsafe_allow_html=True
    )


# ----------- CLEAR HISTORY -----------
if st.session_state.history:

    if st.sidebar.button("🗑️ Clear History"):
        st.session_state.history.clear()
        st.session_state.statistics_reset_at = None
        st.rerun()

    for item in reversed(st.session_state.history):

        style = get_sentiment_style(item["label"])

        st.sidebar.markdown(
            f"""
            <p style="color:{style['color']}; margin:0;">
                {style['emoji']} {item['time']} |
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
        }

        .stButton>button:hover {
            background-color: #45a049;
            cursor: pointer;
        }

        .stProgress>div>div>div>div {
            background-color: #4CAF50;
        }
    </style>
    """,
    unsafe_allow_html=True
)
