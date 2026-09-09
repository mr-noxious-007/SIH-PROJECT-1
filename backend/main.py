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

from providers.other_providers import FuelProvider, CommodityProvider

import pickle

@app.get("/api/dashboard")
def get_dashboard():
    fuel_provider = FuelProvider()
    commodity_provider = CommodityProvider()
    
    fuel_data = fuel_provider.get_fuel_price("VLSFO")
    coal_data = commodity_provider.get_commodity_price("Coal")
    
    # Calculate current live baseline simply
    f_val = fuel_data.get("value")
    c_val = coal_data.get("value")
    
    base_fuel = float(f_val) if isinstance(f_val, (int, float)) else 600.0
    base_coal = float(c_val) if isinstance(c_val, (int, float)) else 135.0
    
    try:
        from services.freight_service import load_ml_model, get_latest_lags_from_db
        model = load_ml_model()
        lags = get_latest_lags_from_db()
        from pandas import DataFrame
        if model and lags:
            vec = DataFrame([{
                'fuel_price': base_fuel,
                'demand_index': base_coal,
                'rate_lag_1': lags['rate_lag_1'],
                'rate_lag_7': lags['rate_lag_7'],
                'fuel_lag_1': lags['fuel_lag_1'],
                'rate_rolling_7d': lags['rate_rolling_7d']
            }])
            current_freight = float(model.predict(vec)[0])
        else:
            current_freight = (base_fuel * 20.0) + (base_coal * 40.0)
    except Exception:
        current_freight = (base_fuel * 20.0) + (base_coal * 40.0)

    # 7/14/30 Day estimates based on momentum (Since model is 1-step ahead, we simulate momentum)
    f_7 = current_freight * 1.01
    f_14 = current_freight * 1.03
    f_30 = current_freight * 1.05
    
    # Load Real Metrics
    metrics_payload = {"mae": "N/A", "rmse": "N/A", "mape": "N/A", "model": "Random Forest"}
    try:
        with open("models/metrics.pkl", "rb") as f:
            metrics = pickle.load(f)
            rf_data = metrics.get("random_forest", {})
            metrics_payload["mae"] = rf_data.get("mae", "N/A")
            metrics_payload["rmse"] = rf_data.get("rmse", "N/A")
            metrics_payload["mape"] = rf_data.get("mape", "N/A")
    except Exception:
        pass

    return {
        "current_rate": round(current_freight, 0),
        "forecast_7d": round(f_7, 0),
        "forecast_14d": round(f_14, 0),
        "forecast_30d": round(f_30, 0),
        "trend": "WAIT/MONITOR" if f_7 < current_freight else "CONSIDER CHARTERING NOW",
        "congestion_paradip": "UNAVAILABLE", # Stripped dummy
        "vessel_availability": "UNAVAILABLE",
        "savings_opportunity": round((f_30 - current_freight) * 20, 0), 
        "data_sources": [fuel_data["source"], coal_data["source"]],
        "ml_performance": metrics_payload
    }

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
