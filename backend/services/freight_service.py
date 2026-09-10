import os
from typing import Dict, Any

from providers.vessel_provider import VesselProvider
from providers.weather_provider import WeatherProvider
from providers.macro_provider import MacroProvider
from providers.other_providers import FreightProvider, PortProvider, FuelProvider, CommodityProvider

class VoyageCostCalculator:
    def __init__(self):
        self.fuel_provider = FuelProvider()
    
    def calculate_voyage_cost(self, vessel_type, cargo_tons, sailing_days):
        # Fetching near-real-time fuel price
        fuel_data = self.fuel_provider.get_fuel_price("VLSFO")
        fuel_price = fuel_data["value"]
        
        # Simple daily cost using actual market fuel proxies (vessel config might modify this)
        daily_cost = 18000 + (fuel_price * 10)  # rough estimation
        
        operating_cost = sailing_days * daily_cost
        positioning_cost = (sailing_days / 2) * daily_cost
        port_fees = operating_cost * 0.025
        total_cost = operating_cost + positioning_cost + port_fees
        
        return {
            "total_voyage_cost": int(total_cost),
            "fuel_price_used": fuel_price,
            "cost_source": fuel_data["source"]
        }


def check_port_compatibility(vessel_type, destination_port):
    """Check if vessel can operate at given port (Static Rule Engine)"""
    vessel_specs = {
        "Handysize": {"draft": 8.2, "loa": 178, "beam": 26},
        "Supramax": {"draft": 9.0, "loa": 189, "beam": 30},
        "Panamax": {"draft": 10.5, "loa": 225, "beam": 32},
        "Capesize": {"draft": 14.0, "loa": 289, "beam": 45}
    }
    port_specs = {
        "Paradip": {"max_draft": 10.5, "max_loa": 225, "max_beam": 32},
        "Haldia": {"max_draft": 8.5, "max_loa": 180, "max_beam": 26}
    }
    
    vessel = vessel_specs.get(vessel_type, vessel_specs["Handysize"])
    port = port_specs.get(destination_port, port_specs["Paradip"])
    
    draft_ok = vessel["draft"] <= port["max_draft"]
    score = 100 if draft_ok else 0
    return {"compatible": draft_ok, "compatibility_score": score, "draft_check": f"draft_ok: {draft_ok}"}


def generate_unified_features(origin, destination, vessel_type):
    weather_provider = WeatherProvider()
    macro_provider = MacroProvider()
    port_provider = PortProvider()
    
    # Example coordinates for weather (Paradip, India)
    weather_data = weather_provider.get_route_weather(20.3, 86.6)
    gdp_data = macro_provider.get_global_gdp_growth()
    port_data = port_provider.get_port_congestion(destination)
    
    return {
        "weather_risk_index": weather_data,
        "global_gdp_growth": gdp_data,
        "port_congestion_index": port_data
    }


import pickle
import pandas as pd
from database import engine

def load_ml_model():
    try:
        with open("models/rf_model.pkl", "rb") as f:
            return pickle.load(f)
    except Exception:
        return None

def get_latest_lags_from_db():
    try:
        query = "SELECT date, fuel_price, demand_index, rate FROM freight_rates ORDER BY date DESC LIMIT 7"
        df = pd.read_sql(query, con=engine)
        if len(df) >= 7:
            return {
                "rate_lag_1": df.iloc[0]['rate'],
                "rate_lag_7": df.iloc[6]['rate'],
                "fuel_lag_1": df.iloc[0]['fuel_price'],
                "rate_rolling_7d": df['rate'].mean()
            }
    except Exception:
        pass
    return None

def generate_recommendation(query):
    """Generates recommendation using the Data Quality Engine."""
    cargo_volume = query.get("cargo_volume_tons", 65000)
    origin = query.get("origin_port", "Australia")
    destination = query.get("destination_port", "Paradip")
    vessel_type = "Supramax"
    
    features = generate_unified_features(origin, destination, vessel_type)
    
    voyage_calculator = VoyageCostCalculator()
    voyage_cost = voyage_calculator.calculate_voyage_cost(vessel_type, cargo_volume, sailing_days=25)
    
    # ------------------
    # ML INFERENCING
    # ------------------
    model = load_ml_model()
    lags = get_latest_lags_from_db()
    
    # Fetch live features from our newly rebuilt Yahoo Finance providers
    fuel_provider = FuelProvider()
    commodity_provider = CommodityProvider()
    
    live_fuel = fuel_provider.get_fuel_price("VLSFO")
    live_coal = commodity_provider.get_commodity_price("Coal")
    
    f_val = live_fuel.get("value", 600.0)
    c_val = live_coal.get("value", 135.0)
    
    current_fuel = float(f_val) if isinstance(f_val, (int, float)) else 600.0
    current_demand = float(c_val) if isinstance(c_val, (int, float)) else 135.0

    predicted_rate = 15.0 # fallback
    ml_status = "UNAVAILABLE"
    recommendation_text = "Insufficient ML data to form recommendation. Use Spot."
    confidence = "UNAVAILABLE"
    
    if model and lags:
        # Create feature vector matching training schema
        # ['fuel_price', 'demand_index', 'rate_lag_1', 'rate_lag_7', 'fuel_lag_1', 'rate_rolling_7d']
        feature_vector = pd.DataFrame([{
            'fuel_price': current_fuel,
            'demand_index': current_demand,
            'rate_lag_1': lags['rate_lag_1'],
            'rate_lag_7': lags['rate_lag_7'],
            'fuel_lag_1': lags['fuel_lag_1'],
            'rate_rolling_7d': lags['rate_rolling_7d']
        }])
        predicted_rate = float(model.predict(feature_vector)[0])
        ml_status = "ACTIVE Model Inference"
        
        # Simple Logic
        if predicted_rate > lags['rate_lag_1'] * 1.05:
            recommendation_text = "CONSIDER CHARTERING NOW (Rates Expected to Rise)"
            confidence = 88
        elif predicted_rate < lags['rate_lag_1'] * 0.95:
            recommendation_text = "WAIT / MONITOR (Rates Expected to Soften)"
            confidence = 82
        else:
            recommendation_text = "FLEXIBLE / MONITOR (Stable Rates)"
            confidence = 75

    predicted_freight_cost = cargo_volume * predicted_rate  

    return {
        "recommended_vessel_type": vessel_type,
        "features": features, 
        "voyage_details": voyage_cost,
        "total_voyage_cost_usd": int(voyage_cost.get("total_voyage_cost", 0) + predicted_freight_cost),
        "confidence_percent": confidence,
        "entry_recommendation": recommendation_text,
        "ml_status": ml_status
    }
