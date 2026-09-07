import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from database import engine, Base

def generate_dummy_data():
    print("Generating FreightIQ DB schema and synthetic data...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    # 1. Indian East Coast & Origin Ports
    ports = [
        {"port_name": "Paradip", "country": "India", "max_draft": 16.0, "max_loa": 260, "max_beam": 33, "handling_rate": 20000, "congestion_index": 30},
        {"port_name": "Visakhapatnam", "country": "India", "max_draft": 18.1, "max_loa": 300, "max_beam": 45, "handling_rate": 35000, "congestion_index": 15},
        {"port_name": "Haldia", "country": "India", "max_draft": 8.5, "max_loa": 180, "max_beam": 26, "handling_rate": 15000, "congestion_index": 45},
        {"port_name": "Newcastle", "country": "Australia", "max_draft": 18.0, "max_loa": 300, "max_beam": 45, "handling_rate": 45000, "congestion_index": 10},
        {"port_name": "Taboneo", "country": "Indonesia", "max_draft": 14.0, "max_loa": 250, "max_beam": 35, "handling_rate": 25000, "congestion_index": 20}
    ]
    pd.DataFrame(ports).to_sql("ports", con=engine, if_exists="append", index=False)
    
    # 2. Vessels Database
    vessels = [
        {"vessel_type": "Handysize", "dwt": 35000, "loa": 190, "beam": 30, "draft": 10, "daily_cost": 14000, "fuel_consumption": 28, "speed": 14.0},
        {"vessel_type": "Supramax", "dwt": 55000, "loa": 200, "beam": 32, "draft": 12, "daily_cost": 18000, "fuel_consumption": 38, "speed": 14.5},
        {"vessel_type": "Panamax", "dwt": 75000, "loa": 225, "beam": 32, "draft": 13.5, "daily_cost": 24000, "fuel_consumption": 52, "speed": 15.0},
        {"vessel_type": "Capesize", "dwt": 180000, "loa": 290, "beam": 45, "draft": 18, "daily_cost": 38000, "fuel_consumption": 95, "speed": 13.5}
    ]
    pd.DataFrame(vessels).to_sql("vessels", con=engine, if_exists="append", index=False)
    
    # 3. Freight Rates Time Series (Realistic Synethtic Data ~ 2 years)
    dates = [datetime(2022, 1, 1).date() + timedelta(days=i) for i in range(1000)]
    np.random.seed(42)
    # Base trend + Seasonality + Random Walk
    rates = 15000 + (np.sin(np.linspace(0, 20, 1000)) * 3000) + np.cumsum(np.random.normal(0, 50, 1000))
    fuel_price = 500 + np.cumsum(np.random.normal(0, 5, 1000))
    demand_index = 100 + (np.sin(np.linspace(0, 50, 1000)) * 20) + np.random.normal(0, 5, 1000)
    
    df_rates = pd.DataFrame({
        "date": dates,
        "route": "Australia -> Paradip",
        "vessel_type": "Panamax",
        "rate": np.round(rates, 2),
        "fuel_price": np.round(fuel_price, 2),
        "demand_index": np.round(demand_index, 2),
        "supply_index": np.round(100 + np.random.normal(0, 2, 1000), 2)
    })
    
    df_rates.to_sql("freight_rates", con=engine, if_exists="append", index=False)
    print("Database seeded with realistic maritime logic successfully!")

if __name__ == "__main__":
    generate_dummy_data()
