def predict_freight_rates(vessel_type, origin, destination, days_ahead=7):
    """Predict freight rates for given route."""
    base_rates = {
        "Handysize": 8.50,
        "Supramax": 9.50,
        "Panamax": 11.00,
        "Capesize": 12.50
    }
    
    base_rate = base_rates.get(vessel_type, 9.50)
    trend_factor = 0.98 if days_ahead <= 7 else 0.95
    
    rate_low = base_rate * trend_factor * 0.92
    rate_high = base_rate * trend_factor * 1.08
    
    confidence = 85 + (10 if days_ahead <= 7 else 5)
    
    return {
        "rate_low": round(rate_low, 2),
        "rate_high": round(rate_high, 2),
        "confidence": min(confidence, 95),
        "trend": "Falling",
        "entry_window": f"Next {max(1, days_ahead-3)}-{days_ahead} days"
    }

def check_port_compatibility(vessel_type, destination_port):
    """Check if vessel can operate at given port"""
    vessel_specs = {
        "Handysize": {"draft": 8.2, "loa": 178, "beam": 26},
        "Supramax": {"draft": 9.0, "loa": 189, "beam": 30},
        "Panamax": {"draft": 10.5, "loa": 225, "beam": 32},
        "Capesize": {"draft": 14.0, "loa": 289, "beam": 45}
    }
    port_specs = {
        "Paradip": {"max_draft": 10.5, "max_loa": 225, "max_beam": 32},
        "Vizag": {"max_draft": 11.0, "max_loa": 240, "max_beam": 33},
        "Gangavaram": {"max_draft": 9.5, "max_loa": 190, "max_beam": 28},
        "Gopalpur": {"max_draft": 9.8, "max_loa": 210, "max_beam": 30},
        "Dhamra": {"max_draft": 9.5, "max_loa": 200, "max_beam": 29},
        "Haldia": {"max_draft": 8.5, "max_loa": 180, "max_beam": 26}
    }
    
    vessel = vessel_specs.get(vessel_type)
    port = port_specs.get(destination_port)
    
    if not vessel or not port:
        return {"compatible": False, "compatibility_score": 0}
    
    draft_ok = vessel["draft"] <= port["max_draft"]
    loa_ok = vessel["loa"] <= port["max_loa"]
    beam_ok = vessel["beam"] <= port["max_beam"]
    
    compatible = draft_ok and loa_ok and beam_ok
    score = 0
    if draft_ok: score += 33
    if loa_ok: score += 33
    if beam_ok: score += 34
    
    return {
        "compatible": compatible,
        "draft_ok": draft_ok,
        "loa_ok": loa_ok,
        "beam_ok": beam_ok,
        "compatibility_score": score,
        "draft_check": f"✓ {vessel['draft']}m <= {port['max_draft']}m" if draft_ok else f"✗ {vessel['draft']}m > {port['max_draft']}m",
        "loa_check": f"✓ {vessel['loa']}m <= {port['max_loa']}m" if loa_ok else f"✗ {vessel['loa']}m > {port['max_loa']}m",
        "beam_check": f"✓ {vessel['beam']}m <= {port['max_beam']}m" if beam_ok else f"✗ {vessel['beam']}m > {port['max_beam']}m"
    }

def calculate_voyage_cost(vessel_type, cargo_tons, sailing_days, daily_cost):
    """Calculate total voyage cost"""
    operating_cost = sailing_days * daily_cost
    positioning_cost = (sailing_days / 2) * daily_cost
    port_fees = operating_cost * 0.025
    insurance = (operating_cost + positioning_cost) * 0.01
    total_cost = operating_cost + positioning_cost + port_fees + insurance
    
    return {
        "operating_cost": int(operating_cost),
        "positioning_cost": int(positioning_cost),
        "port_fees": int(port_fees),
        "insurance": int(insurance),
        "total_voyage_cost": int(total_cost),
        "cost_per_ton": round(total_cost / cargo_tons, 2)
    }

def generate_recommendation(query):
    """Main function: Analyze query and generate recommendation"""
    cargo_volume = query.get("cargo_volume_tons", 65000)
    origin = query.get("origin_port", "Australia")
    destination = query.get("destination_port", "Paradip")
    budget = query.get("budget_usd", 2500000)
    
    rates = predict_freight_rates("Supramax", origin, destination, days_ahead=7)
    compat = check_port_compatibility("Supramax", destination)
    
    voyage_cost = calculate_voyage_cost(
        "Supramax",
        cargo_volume,
        sailing_days=25,
        daily_cost=18000
    )
    
    spot_rate_per_ton = 15.00
    spot_cost = cargo_volume * spot_rate_per_ton
    
    predicted_rate = (rates["rate_low"] + rates["rate_high"]) / 2
    predicted_freight_cost = cargo_volume * predicted_rate
    total_predicted_cost = predicted_freight_cost + voyage_cost["total_voyage_cost"]
    
    savings_usd = spot_cost - total_predicted_cost
    savings_percent = (savings_usd / spot_cost) * 100 if spot_cost > 0 else 0
    
    return {
        "recommended_vessel_type": "Supramax",
        "predicted_rate_low": rates["rate_low"],
        "predicted_rate_high": rates["rate_high"],
        "best_entry_window": rates["entry_window"],
        "estimated_savings_percent": round(savings_percent, 1),
        "estimated_savings_usd": int(savings_usd),
        "port_compatibility_score": compat.get("compatibility_score", 0),
        "draft_check": compat.get("draft_check"),
        "loa_check": compat.get("loa_check"),
        "beam_check": compat.get("beam_check"),
        "estimated_idle_days": 2,
        "total_voyage_cost_usd": voyage_cost["total_voyage_cost"],
        "vs_spot_price_usd": int(spot_cost),
        "confidence_percent": rates["confidence"],
        "entry_recommendation": "Book within next 7 days to lock in low rates"
    }

if __name__ == "__main__":
    import json
    query = {
        "cargo_type": "Coal",
        "cargo_volume_tons": 65000,
        "origin_port": "Australia",
        "destination_port": "Paradip",
        "budget_usd": 2500000,
        "contract_duration_days": 90
    }
    print(json.dumps(generate_recommendation(query), indent=2))
