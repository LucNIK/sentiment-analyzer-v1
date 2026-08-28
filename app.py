# Author: NIKABOU NADJOMBE-CHY
# Date: 2025-09-24

import random
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

MAX_TEXT_LENGTH = 500


# ----------- EXAMPLES -----------
EXAMPLES = [
    "I really love this application. It is fast and easy to use!",
    "This application is excellent and works perfectly.",
    "I am very happy with the results.",
    "I am disappointed with this application.",
    "This application is slow and difficult to use.",
    "The experience was frustrating and confusing.",
    "The application is available today.",
    "The system processed the request successfully.",
    "The weather is cloudy this morning."
]


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

if "example_text" not in st.session_state:
    st.session_state.example_text = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ----------- CLASSIFIER -----------
@st.cache_resource
def load_classifier():
    return pipeline("sentiment-analysis")


classifier = load_classifier()


# ----------- MAIN INTERFACE -----------
st.title("🧠 Sentiment Analyzer")
st.write("Enter a sentence to analyze its sentiment:")


# ----------- QUICK EXAMPLES -----------
st.markdown("### 💡 Quick Examples")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("😄 Positive"):
        st.session_state.example_text = EXAMPLES[0]
        st.rerun()

with col2:
    if st.button("😢 Negative"):
        st.session_state.example_text = EXAMPLES[4]
        st.rerun()

with col3:
    if st.button("🎲 Random"):
        st.session_state.example_text = random.choice(EXAMPLES)
        st.rerun()


# ----------- NEW ANALYSIS -----------
if st.session_state.last_result:

    if st.button("🔄 Analyze another text"):
        st.session_state.example_text = ""
        st.session_state.last_result = None
        st.rerun()


# ----------- INPUT FORM -----------
with st.form("sentiment_form", clear_on_submit=True):

    user_input = st.text_area(
        "Your text:",
        value=st.session_state.example_text,
        max_chars=MAX_TEXT_LENGTH,
        height=120
    )

    character_count = len(user_input)
    word_count = len(user_input.split())

    percentage = min(
        character_count / MAX_TEXT_LENGTH,
        1.0
    )

    st.progress(percentage)

    st.caption(
        f"📝 {word_count} words • "
        f"{character_count}/{MAX_TEXT_LENGTH} characters"
    )

    submitted = st.form_submit_button("Analyze")


# ----------- ANALYSIS -----------
if submitted:

    user_input = user_input.strip()

    st.session_state.example_text = ""

    if not user_input:

        st.warning(
            "Please enter some text before analyzing."
        )

    elif len(user_input) > MAX_TEXT_LENGTH:

        st.error(
            f"Text is too long. Please keep it under "
            f"{MAX_TEXT_LENGTH} characters."
        )

    else:

        try:

            progress_bar = st.progress(0)
            status_text = st.empty()

            for percent in range(0, 101, 10):

                time.sleep(0.05)

                progress_bar.progress(percent)

                status_text.text(
                    f"Analyzing... {percent}%"
                )

            progress_bar.empty()
            status_text.empty()

            analysis_start = time.perf_counter()

            result = classifier(user_input)[0]

            analysis_time = (
                time.perf_counter()
                - analysis_start
            )

            label = result["label"].upper()
            score = result["score"]

            sentiment = get_sentiment_style(label)

            # ----------- RESULT -----------
            st.markdown(
                f"""
                <div style="
                    padding:20px;
                    border-radius:12px;
                    border-left:6px solid
                    {sentiment['color']};
                    background-color:
                    rgba(128,128,128,0.08);
                ">

                    <h2 style="
                        color:{sentiment['color']};
                    ">
                        {sentiment['emoji']} {label}
                    </h2>

                    <p>
                        {sentiment['message']}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown("### Confidence")

            st.progress(score)

            st.markdown(
                f"**{score * 100:.1f}%**"
            )

            st.caption(
                f"⚡ Analysis completed in "
                f"{analysis_time:.3f} seconds"
            )

            # ----------- SUMMARY -----------
            st.markdown("### 📋 Analysis Summary")

            summary = (
                f"Sentiment: {label}\n"
                f"Confidence: {score * 100:.1f}%\n"
                f"Words: {len(user_input.split())}\n"
                f"Characters: {len(user_input)}\n"
                f"Analysis time: {analysis_time:.3f}s"
            )

            st.code(
                summary,
                language="text"
            )

            # ----------- LAST RESULT -----------
            st.session_state.last_result = {
                "text": user_input,
                "label": label,
                "score": score,
                "analysis_time": analysis_time
            }

            # ----------- HISTORY -----------
            st.session_state.history.append(
                {
                    "text": user_input,
                    "label": label,
                    "score": score,
                    "time": datetime.now().strftime(
                        "%H:%M:%S"
                    ),
                    "created_at": datetime.now(),
                    "analysis_time": analysis_time
                }
            )

        except Exception as error:

            st.error(
                "An error occurred while analyzing "
                "the text. Please try again."
            )

            st.caption(
                f"Error details: {error}"
            )


# ----------- SIDEBAR -----------
st.sidebar.title("📜 History")


# ----------- STATISTICS DATA -----------
if st.session_state.statistics_reset_at:

    statistics_history = [
        item
        for item in st.session_state.history
        if item["created_at"]
        > st.session_state.statistics_reset_at
    ]

else:

    statistics_history = (
        st.session_state.history
    )


analysis_count = len(
    statistics_history
)

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


# ----------- COUNTER -----------
st.sidebar.metric(
    "📊 Analyses",
    analysis_count
)


# ----------- STATISTICS -----------
st.sidebar.markdown(
    "### 📈 Sentiment Statistics"
)

st.sidebar.markdown(
    f"😄 **Positive:** {positive_count}"
)

st.sidebar.markdown(
    f"😢 **Negative:** {negative_count}"
)

st.sidebar.markdown(
    f"😐 **Neutral:** {neutral_count}"
)


# ----------- RESET STATISTICS -----------
if st.sidebar.button(
    "🔄 Reset Statistics"
):

    st.session_state.statistics_reset_at = (
        datetime.now()
    )

    st.rerun()


# ----------- LAST RESULT -----------
if st.session_state.last_result:

    last_result = (
        st.session_state.last_result
    )

    last_style = get_sentiment_style(
        last_result["label"]
    )

    st.sidebar.markdown(
        "### 🔎 Last Analysis"
    )

    st.sidebar.markdown(
        f"""
        <div style="
            padding:10px;
            border-left:4px solid
            {last_style['color']};
            border-radius:6px;
            background-color:
            rgba(128,128,128,0.08);
        ">

            <strong>
                {last_style['emoji']}
                {last_result['label']}
            </strong>

            <br>

            Confidence:
            {last_result['score'] * 100:.1f}%

            <br>

            Characters:
            {len(last_result['text'])}

            <br>

            Words:
            {len(last_result['text'].split())}

            <br>

            Analysis time:
            {last_result['analysis_time']:.3f}s

        </div>
        """,
        unsafe_allow_html=True
    )


# ----------- CLEAR HISTORY -----------
if st.session_state.history:

    if st.sidebar.button(
        "🗑️ Clear History"
    ):

        st.session_state.history.clear()

        st.session_state.last_result = None

        st.session_state.statistics_reset_at = (
            None
        )

        st.rerun()

    for item in reversed(
        st.session_state.history
    ):

        style = get_sentiment_style(
            item["label"]
        )

        st.sidebar.markdown(
            f"""
            <p style="
                color:{style['color']};
                margin:0;
            ">
                {style['emoji']}
                {item['time']} |
                {item['label']}
                ({item['score'] * 100:.1f}%)
            </p>

            <p style="
                margin-left:10px;
            ">
                {item['text']}
            </p>

            <hr style="
                border:1px solid #ccc;
            ">
            """,
            unsafe_allow_html=True
        )

else:

    st.sidebar.write(
        "No history yet. Submit a sentence "
        "to see it here."
    )


# ----------- STYLING -----------
st.markdown(
    """
    <style>

        .stTextInput>div>div>input,
        .stTextArea textarea {

            font-size:1.1rem;

            padding-left:10px;

            border-radius:10px;

        }

        .stButton>button {

            background-color:#4CAF50;

            color:white;

            font-size:1.1rem;

            padding:10px 20px;

            border-radius:8px;

        }

        .stButton>button:hover {

            background-color:#45a049;

            cursor:pointer;

        }

        .stProgress>div>div>div>div {

            background-color:#4CAF50;

        }

    </style>
    """,
    unsafe_allow_html=True
)
