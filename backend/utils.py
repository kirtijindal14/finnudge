# backend/utils.py
import joblib
import torch
import open_clip
import pytesseract
import scipy.sparse as sp
import numpy as np
from PIL import Image

def load_models():
    model_data = joblib.load("data/finnudge_final_model.pkl")
    clip_model, preprocess, _ = open_clip.create_model_and_transforms(
        'ViT-B-32', pretrained='openai'
    )
    clip_model.eval()
    return {"model_data": model_data, "clip": clip_model, "preprocess": preprocess}

def predict_pattern(image, models):
    clip_model = models["clip"]
    preprocess = models["preprocess"]
    model_data = models["model_data"]
    
    img_tensor = preprocess(image).unsqueeze(0)
    with torch.no_grad():
        emb = clip_model.encode_image(img_tensor)
        emb = emb / emb.norm(dim=-1, keepdim=True)
    emb = emb.squeeze().numpy()
    
    try:
        ocr_text = pytesseract.image_to_string(image)
    except:
        ocr_text = ""
    
    clf = model_data["classifier"]
    tfidf = model_data["tfidf"]
    text_features = tfidf.transform([ocr_text])
    X = sp.hstack([sp.csr_matrix(emb.reshape(1,-1)), text_features])
    
    pred = clf.predict(X)[0]
    proba = clf.predict_proba(X)[0]
    confidence = round(float(max(proba)) * 100, 1)
    
    return pred, confidence, ocr_text

def calculate_nudge_score(pattern, severity=2):
    base = {'CLEAN':0,'DEFAULT':15,'ANCHOR':20,'GAMIFY':25,'LOSS':35,'SCARCITY':40,'FOMO':45}
    return min(base.get(pattern, 0) * severity, 100)

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
    return {
        "clean": round(clean),
        "nudged": round(max(clean - total_loss, 0)),
        "loss": round(total_loss)
    }