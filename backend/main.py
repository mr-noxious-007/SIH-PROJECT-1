import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any
import random

from providers.weather_provider import WeatherProvider
from providers.macro_provider import MacroProvider
from providers.vessel_provider import VesselProvider
from services.freight_service import generate_recommendation

app = FastAPI(title="FreightIQ API Real-Time Hybrid Engine")

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

@app.get("/api/weather/route")
def get_weather(lat: float = 20.3, lon: float = 86.6):
    provider = WeatherProvider()
    return provider.get_route_weather(lat, lon)

@app.get("/api/macro/gdp")
def get_gdp():
    provider = MacroProvider()
    return provider.get_global_gdp_growth()

@app.get("/api/vessels/availability")
def get_vessels(port: str = "Paradip", vessel_type: str = "Supramax"):
    provider = VesselProvider()
    return provider.get_available_vessels(port, vessel_type)

@app.post("/api/chartering/recommend")
def recommend_charter(query: CharterQuery):
    result = generate_recommendation(query.dict())
    return result

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
