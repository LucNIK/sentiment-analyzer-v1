Author: NIKABOU NADJOMBE
Date: 2025-09-24
# 🧠 Sentiment Analyzer Dashboard (v1)

A professional, interactive Sentiment Analyzer built with **Streamlit** and **HuggingFace Transformers**.

## Features v1
- Analyze sentiment (POSITIVE/NEGATIVE/NEUTRAL) with emojis.
- Horizontal KPI-style score bars.
- Animated progress bar during analysis.
- Sidebar history of previous analyses with timestamps.
- Dark/Light theme toggle.
- Modern UI with hover effects on buttons and input.

## Installation

1. Clone the repo:

```bash
git clone https://github.com/<nik552>/sentiment-analyzer.git
cd sentiment-analyzer
```


Create a virtual environment (optional but recommended):

python -m venv venv
source venv/Scripts/activate   # Windows


Install dependencies:

pip install -r requirements.txt


Run the app:

streamlit run app.py

Notes

Requires a HuggingFace token if using private models: https://huggingface.co/settings/tokens

Python 3.13+ recommended