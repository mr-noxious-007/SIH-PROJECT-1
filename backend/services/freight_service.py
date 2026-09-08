import os
from typing import Dict, Any

from providers.vessel_provider import VesselProvider
from providers.weather_provider import WeatherProvider
from providers.macro_provider import MacroProvider
from providers.other_providers import FreightProvider, PortProvider, FuelProvider

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


def generate_recommendation(query):
    """Generates recommendation using the Data Quality Engine."""
    cargo_volume = query.get("cargo_volume_tons", 65000)
    origin = query.get("origin_port", "Australia")
    destination = query.get("destination_port", "Paradip")
    vessel_type = "Supramax"
    
    features = generate_unified_features(origin, destination, vessel_type)
    
    voyage_calculator = VoyageCostCalculator()
    voyage_cost = voyage_calculator.calculate_voyage_cost(vessel_type, cargo_volume, sailing_days=25)
    
    # Connecting to ML Model pipeline (Assuming the trained model handles feature vectors)
    # Using fallback dummy rate for compilation without ML inferencing setup
    predicted_freight_cost = cargo_volume * 15.0  

    return {
        "recommended_vessel_type": vessel_type,
        "features": features, # Contains data_quality metadata natively
        "voyage_details": voyage_cost,
        "total_voyage_cost_usd": voyage_cost["total_voyage_cost"],
        "confidence_percent": 85,
        "entry_recommendation": "Calculated using real/fallback hybrid variables."
    }
