import streamlit as st
import numpy as np
import joblib
import torch
import open_clip
import pytesseract
import scipy.sparse as sp
from PIL import Image

st.set_page_config(
    page_title="FinNudge — Screenshot Analyser",
    page_icon="🔍",
    layout="wide"
)

# Back button
st.markdown("""
    <a href='https://finnudge.vercel.app' style='color:#4A9EFF;text-decoration:none;font-size:14px'>
        ← Back to FinNudge
    </a>
""", unsafe_allow_html=True)

st.title("🔍 FinNudge — Screenshot Analyser")
st.markdown("Upload any Indian investment app screenshot to detect dark patterns.")
st.divider()

@st.cache_resource
def get_models():
    model_data = joblib.load("data/finnudge_final_model.pkl")
    clip_model, preprocess, _ = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='openai'
    )
    clip_model.eval()
    return model_data, clip_model, preprocess

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
    base = {'CLEAN':0,'DEFAULT':15,'ANCHOR':20,'GAMIFY':25,'LOSS':35,'SCARCITY':40,'FOMO':45}
    return min(base.get(pattern, 0) * severity, 100)

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
    return pred, confidence, calculate_nudge_score(pred), text

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

bias_map = {
    'FOMO': ('Social Proof / Herd Behaviour', '👥'),
    'LOSS': ('Loss Aversion (Kahneman & Tversky)', '📉'),
    'ANCHOR': ('Anchoring Bias', '⚓'),
    'SCARCITY': ('Scarcity Heuristic', '⏰'),
    'GAMIFY': ('Variable Reward Loop', '🎮'),
    'DEFAULT': ('Status Quo / Default Bias', '🔘'),
    'CLEAN': ('No manipulation detected', '✅')
}

model_data, clip_model, preprocess = get_models()

col1, col2 = st.columns([1, 1])

with col1:
    uploaded = st.file_uploader("Upload a fintech app screenshot", type=["png", "jpg", "jpeg"])
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
                f"⚠️ This pattern could cost you **₹{loss:,}** over 10 years.\n\n"
                f"Rational corpus: ₹{clean:,} → Nudged corpus: ₹{nudged:,}"
            )
        else:
            st.success("✅ Clean screen — no dark patterns detected!")

        with st.expander("OCR Text Extracted"):
            st.text(ocr_text[:500] if ocr_text else "No text extracted")

st.divider()
st.caption("FinNudge — Built by Kirti Jindal | NSUT Delhi | Part of finnudge.vercel.app")