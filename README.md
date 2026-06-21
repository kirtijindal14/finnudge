# 🔍 FinNudge — Behavioural Finance Audit of Indian Investment Apps

> *"Dark patterns in Indian investment apps cost retail investors ₹2.4L over 10 years — without them ever realising it."*

**Live Demo:** [finnudge.vercel.app](https://finnudge.vercel.app) | **ML Analyser:** [finnudge.streamlit.app](https://finnudge.streamlit.app)

---

## What is FinNudge?

FinNudge audits Indian investment apps (Groww, Zerodha, Upstox, INDmoney, AngelOne) for **dark patterns** — design tricks that exploit cognitive biases to make users invest impulsively. It then calculates the **real rupee cost** these patterns impose on retail investors over time.

---

## Key Findings

| App | NudgeScore | Risk | 10-Year Hidden Cost |
|---|---|---|---|
| Groww | 42.5/100 | 🔴 High | ₹3.5L |
| AngelOne | 40.6/100 | 🔴 High | ₹3.5L |
| INDmoney | 29.5/100 | 🟡 Moderate | ₹1.2L |
| Upstox | 28.0/100 | 🟡 Moderate | ₹1.2L |
| Zerodha | 12.5/100 | 🟢 Low | ₹0.6L |

**A retail investor on Groww loses 6x more wealth to dark patterns than one on Zerodha.**

---

## Dark Pattern Categories

| Pattern | Bias Exploited | Example |
|---|---|---|
| FOMO | Social Proof | "2,847 people bought this today" |
| LOSS | Loss Aversion | Portfolio loss in large red numbers |
| ANCHOR | Anchoring Bias | "This fund gave 87% in 2023" |
| SCARCITY | Scarcity Heuristic | Countdown timer on IPO |
| GAMIFY | Variable Reward Loop | Scratch cards after transactions |
| DEFAULT | Status Quo Bias | Giant "ADD FUNDS" button |

---

## Tech Stack
Frontend        Backend         ML Pipeline

──────────      ───────────     ────────────

React + Vite    FastAPI         CLIP (ViT-B-32)

Tailwind CSS    Python          OCR (Tesseract)

Recharts        Render          TF-IDF

Vercel          REST API        Random Forest

---

## Architecture
User uploads screenshot

↓

CLIP Model → 512D visual embeddings

+

Tesseract OCR → text → TF-IDF (200D)

↓

Combined 712D feature vector

↓

Random Forest Classifier

↓

Pattern label + NudgeScore + Finance Impact

---

## ML Pipeline

- **Dataset:** 104 manually labelled screenshots across 5 Indian investment apps
- **Feature extraction:** OpenAI CLIP (ViT-B-32) visual embeddings + TF-IDF OCR text
- **Classifier:** Random Forest with class balancing
- **Cross-validated accuracy:** 54.71% (3.8x above random baseline of 14.3%)
- **Best performing classes:** GAMIFY (F1=0.83), LOSS (F1=0.80)

---

## Finance Impact Model

Dark patterns cause fund switches → each switch incurs:
- **Exit load** (1% of corpus)
- **Short-term capital gains tax** (20% on gains)
- **Compounding loss** (missed growth on withdrawn corpus)
Base case: ₹5,000/month SIP | 12% returns | 4 switches/year

Without dark patterns: ₹11,61,695

With dark patterns:    ₹9,25,178

Hidden cost:           ₹2,36,517 (20.4% of wealth)

---

## Project Structure
FinNudge/

├── frontend/          # React + Vite + Tailwind (Vercel)

│   └── src/

│       ├── App.jsx

│       └── components/

│           ├── Analyser.jsx

│           ├── Rankings.jsx

│           └── Finance.jsx

├── backend/           # FastAPI (Render)

│   ├── main.py

│   └── utils.py

├── app/               # Streamlit ML Analyser

│   └── streamlit_app.py

├── notebooks/         # Research notebooks

│   ├── 02_clip_embeddings.ipynb

│   ├── 03_classifier.ipynb

│   └── 04_finance_model.ipynb

├── data/              # Dataset + models

│   ├── labelled.csv

│   ├── embeddings.npy

│   └── finnudge_final_model.pkl

└── report/            # Charts + visualisations

├── app_ranking.png

├── wealth_gap_chart.png

└── investor_profiles.png

---

## Setup

```bash
git clone https://github.com/kirtijindal14/finnudge.git
cd finnudge

# Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev

# ML Analyser
streamlit run app/streamlit_app.py
```

---

## Built By

**Kirti Jindal** | B.Tech CSE, NSUT Delhi (CGPA: 8.47)

[LinkedIn](https://linkedin.com/in/kirtijindal14) | [GitHub](https://github.com/kirtijindal14)

---

*FinNudge — Placement Project 2026*
