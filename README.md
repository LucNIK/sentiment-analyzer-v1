Author: NIKABOU NADJOMBE
Date: 2025-09-24
1️⃣ README.md
# Sentiment Analyzer v1

🧠 **AI-powered real-time sentiment analyzer** built with Python and Streamlit.  
Visualizes sentiment as **POSITIVE, NEUTRAL, NEGATIVE**, shows **confidence scores**, and maintains a **history of analyzed sentences**.

---

## Features

- Real-time sentiment analysis using Hugging Face Transformers
- Interactive **Streamlit dashboard**
- Visual indicators:
  - Emojis 😄😐😢 according to sentiment
  - Horizontal KPI-style confidence bars
- History panel to track previous analyses
- Dark/light mode toggle
- Clear input field after each submission

---

## Installation

1. Clone this repository:
```bash
git clone https://github.com/<your-username>/sentiment-analyzer.git
cd sentiment-analyzer```


Create a virtual environment (optional but recommended):

python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux


Install dependencies:

pip install -r requirements.txt


Make sure you have a Hugging Face token for private models (if needed):

hf auth login

Usage
streamlit run app.py


Enter a sentence in the input box

Click Analyze

View sentiment, confidence bar, emoji, and history

Dark/light mode toggle available in the sidebar

Screenshots

Requirements

See requirements.txt for all dependencies.

License

MIT License


---

### **2️⃣ `requirements.txt`**

```txt
streamlit>=1.26.0
transformers>=4.35.0
torch>=2.1.0
tensorflow>=2.14.0
tf-keras>=2.14.0
numpy>=1.26.0
pandas>=2.1.0