from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FinNudge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.get("/")
def root():
    return {"message": "FinNudge API running"}

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