# app/streamlit_app.py
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import torch
import open_clip
import pytesseract
import json
import scipy.sparse as sp
import matplotlib.pyplot as plt
from PIL import Image

st.set_page_config(
    page_title="FinNudge — Dark Pattern Auditor",
    page_icon="🔍",
    layout="wide"
)

# ── CORE LOGIC (will become FastAPI endpoints later) ──────────────────────

def load_models():
    model_data = joblib.load("data/finnudge_final_model.pkl")
    clip_model, preprocess, _ = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='openai'
    )
    clip_model.eval()
    return model_data, clip_model, preprocess

@st.cache_resource
def get_models():
    return load_models()

def get_clip_embedding(image, clip_model, preprocess):
    img_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        emb = clip_model.encode_image(img_tensor)
        emb = emb / emb.norm(dim=-1, keepdim=True)
    return emb.squeeze().numpy()

def get_ocr_text(image):
    try:
        return pytesseract.image_to_string(image)
    except:
        return ""

def calculate_nudge_score(pattern, severity=2):
    base_scores = {
        'CLEAN': 0, 'DEFAULT': 15, 'ANCHOR': 20,
        'GAMIFY': 25, 'LOSS': 35, 'SCARCITY': 40, 'FOMO': 45
    }
    return min(base_scores.get(pattern, 0) * severity, 100)

def predict_pattern(image, model_data, clip_model, preprocess):
    emb = get_clip_embedding(image, clip_model, preprocess)
    text = get_ocr_text(image)
    clf = model_data['classifier']
    tfidf = model_data['tfidf']
    text_features = tfidf.transform([text])
    X = sp.hstack([sp.csr_matrix(emb.reshape(1,-1)), text_features])
    pred = clf.predict(X)[0]
    proba = clf.predict_proba(X)[0]
    confidence = round(max(proba) * 100, 1)
    nudge_score = calculate_nudge_score(pred)
    return pred, confidence, nudge_score, text

def calculate_finance_impact(nudge_score, years=10, monthly=5000):
    switches = 6 if nudge_score > 40 else 4 if nudge_score > 25 else 1
    r = 0.12 / 12
    months = years * 12
    clean = monthly * (((1+r)**months - 1)/r) * (1+r)
    avg_corpus = monthly * 6
    cost_per_switch = (
        avg_corpus * 0.01 +
        avg_corpus * 0.08 * 0.20 +
        avg_corpus * ((1.12)**years - (1.12)**(years-0.5))
    )
    total_loss = cost_per_switch * switches * years
    return round(clean), round(max(clean - total_loss, 0)), round(total_loss)

# ── BIAS MAP ──────────────────────────────────────────────────────────────
bias_map = {
    'FOMO': ('Social Proof / Herd Behaviour', '👥'),
    'LOSS': ('Loss Aversion (Kahneman & Tversky)', '📉'),
    'ANCHOR': ('Anchoring Bias', '⚓'),
    'SCARCITY': ('Scarcity Heuristic', '⏰'),
    'GAMIFY': ('Variable Reward Loop', '🎮'),
    'DEFAULT': ('Status Quo / Default Bias', '🔘'),
    'CLEAN': ('No manipulation detected', '✅')
}

# ── UI ────────────────────────────────────────────────────────────────────
st.title("🔍 FinNudge")
st.markdown("#### Behavioural Finance Audit of Indian Investment Apps")
st.markdown("Upload any screenshot from an Indian investment app to detect dark patterns and calculate their financial impact.")
st.divider()

model_data, clip_model, preprocess = get_models()

tab1, tab2, tab3 = st.tabs(["🔍 Analyse Screenshot", "📊 App Rankings", "💰 Finance Impact"])

# ── TAB 1 — Screenshot Analyser ──────────────────────────────────────────
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        uploaded = st.file_uploader(
            "Upload a fintech app screenshot",
            type=["png", "jpg", "jpeg"]
        )
        if uploaded:
            image = Image.open(uploaded).convert("RGB")
            st.image(image, caption="Uploaded Screenshot", use_column_width=True)
    
    with col2:
        if uploaded:
            with st.spinner("Analysing..."):
                pred, confidence, nudge_score, ocr_text = predict_pattern(
                    image, model_data, clip_model, preprocess
                )
                clean, nudged, loss = calculate_finance_impact(nudge_score)
            
            bias_name, bias_icon = bias_map.get(pred, ('Unknown', '❓'))
            color = "🔴" if nudge_score > 60 else "🟡" if nudge_score > 30 else "🟢"
            
            st.subheader("Analysis Result")
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Pattern", f"{bias_icon} {pred}")
            m2.metric("NudgeScore", f"{nudge_score}/100 {color}")
            m3.metric("Confidence", f"{confidence}%")
            
            st.info(f"**Bias Exploited:** {bias_name}")
            
            if pred != 'CLEAN':
                st.error(
                    f"⚠️ This pattern could cost you **₹{loss:,}** "
                    f"over 10 years if acted on regularly.\n\n"
                    f"Rational corpus: ₹{clean:,} → Nudged corpus: ₹{nudged:,}"
                )
            else:
                st.success("✅ This screen appears clean — no dark patterns detected!")
            
            with st.expander("OCR Text Extracted"):
                st.text(ocr_text[:500] if ocr_text else "No text extracted")

# ── TAB 2 — App Rankings ─────────────────────────────────────────────────
with tab2:
    st.subheader("App NudgeScore Ranking")
    st.markdown("Based on analysis of 104 labelled screenshots across 5 Indian investment apps.")
    
    app_data = {
        'App': ['Groww', 'AngelOne', 'INDmoney', 'Upstox', 'Zerodha'],
        'NudgeScore': [42.5, 40.6, 29.5, 28.0, 12.5],
        'Risk': ['🔴 High', '🔴 High', '🟡 Moderate', '🟡 Moderate', '🟢 Low'],
        'Top Pattern': ['DEFAULT', 'DEFAULT', 'DEFAULT', 'GAMIFY', 'GAMIFY'],
        '10yr Loss': ['₹3.5L', '₹3.5L', '₹1.2L', '₹1.2L', '₹0.6L']
    }
    
    df = pd.DataFrame(app_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    colors = ['#C0392B','#C0392B','#E8A838','#E8A838','#1A7A4A']
    ax.barh(df['App'], df['NudgeScore'], color=colors)
    ax.set_xlabel('NudgeScore (0-100)')
    ax.set_title('App Manipulation Score', fontweight='bold')
    ax.axvline(x=35, color='red', linestyle='--', alpha=0.5)
    for i, (app, score) in enumerate(zip(df['App'], df['NudgeScore'])):
        ax.text(score + 0.3, i, f'{score}', va='center', fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)

# ── TAB 3 — Finance Impact ───────────────────────────────────────────────
with tab3:
    st.subheader("Calculate Your Dark Pattern Cost")
    
    col1, col2 = st.columns(2)
    with col1:
        monthly = st.slider("Monthly SIP (₹)", 1000, 20000, 5000, 500)
        years = st.slider("Investment Horizon (years)", 1, 20, 10)
    with col2:
        app_choice = st.selectbox(
            "Which app do you use?",
            ['Groww', 'AngelOne', 'INDmoney', 'Upstox', 'Zerodha']
        )
    
    score_map = {'Groww': 42.5, 'AngelOne': 40.6, 
                 'INDmoney': 29.5, 'Upstox': 28.0, 'Zerodha': 12.5}
    app_score = score_map[app_choice]
    clean, nudged, loss = calculate_finance_impact(app_score, years, monthly)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Without Dark Patterns", f"₹{clean:,}")
    m2.metric("With Dark Patterns", f"₹{nudged:,}", delta=f"-₹{loss:,}", delta_color="inverse")
    m3.metric("Hidden Cost", f"₹{loss:,}")
    
    # Wealth gap chart
    years_r = list(range(0, years+1))
    clean_v, nudged_v = [], []
    for y in years_r:
        if y == 0:
            clean_v.append(0)
            nudged_v.append(0)
        else:
            c, n, _ = calculate_finance_impact(app_score, y, monthly)
            clean_v.append(c/100000)
            nudged_v.append(n/100000)
    
    fig2, ax2 = plt.subplots(figsize=(10, 5))
    ax2.plot(years_r, clean_v, 'g-o', linewidth=2, label='Without Dark Patterns')
    ax2.plot(years_r, nudged_v, 'r-o', linewidth=2, label=f'Using {app_choice}')
    ax2.fill_between(years_r, nudged_v, clean_v, alpha=0.15, color='red')
    ax2.set_xlabel('Years')
    ax2.set_ylabel('Corpus (₹ Lakhs)')
    ax2.set_title(f'Wealth Gap — {app_choice} vs Rational Investor', fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig2)

st.divider()
st.caption("FinNudge — Built by Kirti Jindal | NSUT Delhi" )
           