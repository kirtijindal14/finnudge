from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from backend.utils import load_models, predict_pattern, calculate_nudge_score, calculate_finance_impact
from PIL import Image
import io

app = FastAPI(title="FinNudge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

models = load_models()

@app.get("/")
def root():
    return {"message": "FinNudge API running"}

@app.post("/api/analyse")
async def analyse(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    pred, confidence, ocr_text = predict_pattern(image, models)
    nudge_score = calculate_nudge_score(pred)
    finance = calculate_finance_impact(nudge_score)
    return {
        "pattern": pred,
        "confidence": confidence,
        "nudge_score": nudge_score,
        "ocr_text": ocr_text[:200],
        "finance": finance
    }

@app.get("/api/rankings")
def rankings():
    return {
        "apps": [
            {"name": "Groww",    "score": 42.5, "risk": "High",     "loss": "₹3.5L"},
            {"name": "AngelOne", "score": 40.6, "risk": "High",     "loss": "₹3.5L"},
            {"name": "INDmoney", "score": 29.5, "risk": "Moderate", "loss": "₹1.2L"},
            {"name": "Upstox",   "score": 28.0, "risk": "Moderate", "loss": "₹1.2L"},
            {"name": "Zerodha",  "score": 12.5, "risk": "Low",      "loss": "₹0.6L"},
        ]
    }

@app.get("/api/finance")
def finance(monthly: int = 5000, years: int = 10, app: str = "Groww"):
    score_map = {
        "Groww": 42.5, "AngelOne": 40.6,
        "INDmoney": 29.5, "Upstox": 28.0, "Zerodha": 12.5
    }
    score = score_map.get(app, 30)

    # Build chart data
    chart_data = []
    for y in range(0, years + 1):
        if y == 0:
            chart_data.append({"year": 0, "clean": 0, "nudged": 0})
        else:
            r = calculate_finance_impact(score, y, monthly)
            chart_data.append({
                "year": y,
                "clean": round(r["clean"] / 100000, 2),
                "nudged": round(r["nudged"] / 100000, 2)
            })

    base = calculate_finance_impact(score, years, monthly)
    return {
        "clean": base["clean"],
        "nudged": base["nudged"],
        "loss": base["loss"],
        "chart_data": chart_data
    }