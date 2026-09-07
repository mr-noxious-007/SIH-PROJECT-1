from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI(title="FreightIQ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CharterQuery(BaseModel):
    commodity: str
    cargo_quantity: int
    origin: str
    loading_port: str
    destination: str
    contract_type: str
    voyages: int

@app.get("/api/dashboard")
def get_dashboard():
    return {
        "current_rate": 18200,
        "forecast_7d": 18900,
        "forecast_14d": 20100,
        "forecast_30d": 21400,
        "trend": "Bullish",
        "congestion_paradip": "30%",
        "vessel_availability": 142,
        "savings_opportunity": 420000
    }

@app.post("/api/chartering/recommend")
def recommend_charter(query: CharterQuery):
    # Logic matching SIH Demo prompt constraints exactly
    is_haldia = query.destination.lower() == "haldia"
    vessel = "Handysize" if is_haldia else "Panamax" if query.cargo_quantity > 60000 else "Supramax"
    
    return {
        "recommended_vessel": vessel,
        "recommended_contract": "3-Month Multi-Voyage",
        "recommended_entry": "Enter within next 5 days",
        "current_freight_per_day": 18200,
        "forecast_30d_freight_per_day": 21100,
        "expected_savings": 233500,
        "port_compatibility": [
            {"port": query.loading_port, "compatible": True},
            {"port": query.destination, "compatible": not is_haldia or vessel == "Handysize"}
        ],
        "expected_turnaround": 9.1,
        "idle_risk": "LOW",
        "deadheading_risk": "LOW",
        "market_risk": "MEDIUM",
        "overall_recommendation": "ENTER MULTI-VOYAGE CONTRACT NOW",
        "explanation": f"Freight rates are forecast to increase by approximately {(21100-18200)/18200*100:.1f}% over 30 days. Securing a multi-voyage contract shields against market volatility."
    }

@app.get("/api/forecast/comparison")
def get_forecast_comparison():
    # Returns generated dummy metrics
    return [
        {"model": "ARIMA", "mae": 520, "rmse": 710},
        {"model": "XGBoost", "mae": 340, "rmse": 480},
        {"model": "LSTM", "mae": 290, "rmse": 410}
    ]

@app.get("/api/forecast/chart")
def get_forecast_chart():
    # Return time-series data for recharts
    data = []
    base = 15000
    for i in range(1, 31):
        data.append({
            "day": f"Day {i}",
            "historical": base + random.randint(-500, 500) if i <= 10 else None,
            "forecast_7d": base + i * 50 if i > 10 and i <= 17 else None,
            "forecast_14d": base + i * 80 if i > 10 and i <= 24 else None,
            "forecast_30d": base + i * 110 if i > 10 else None,
        })
    return data

@app.get("/api/features/importance")
def get_feature_importance():
    return [
        {"feature": "Demand Index", "importance": 32},
        {"feature": "Port Congestion", "importance": 24},
        {"feature": "Fuel Price", "importance": 18},
        {"feature": "Supply Index", "importance": 14},
        {"feature": "Seasonality", "importance": 8},
        {"feature": "Oil Price", "importance": 4}
    ]
