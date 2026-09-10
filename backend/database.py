from sqlalchemy import create_engine, Column, Integer, String, Float, Date, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./freightiq.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Port(Base):
    __tablename__ = "ports"
    id = Column(Integer, primary_key=True, index=True)
    port_name = Column(String, index=True)
    country = Column(String)
    max_draft = Column(Float)
    max_loa = Column(Float)
    max_beam = Column(Float)
    handling_rate = Column(Float)
    congestion_index = Column(Float, default=0.0)

class Vessel(Base):
    __tablename__ = "vessels"
    id = Column(Integer, primary_key=True, index=True)
    vessel_type = Column(String, index=True)
    dwt = Column(Integer)
    loa = Column(Float)
    beam = Column(Float)
    draft = Column(Float)
    daily_cost = Column(Float)
    fuel_consumption = Column(Float)
    speed = Column(Float)

class FreightRate(Base):
    __tablename__ = "freight_rates"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    route = Column(String, index=True)
    vessel_type = Column(String, index=True)
    rate = Column(Float)
    fuel_price = Column(Float)
    demand_index = Column(Float)
    supply_index = Column(Float)

class DataSource(Base):
    __tablename__ = "data_sources"
    id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String, index=True)
    status = Column(String)
    last_update = Column(Date)
    data_quality = Column(String)

class ForecastFeature(Base):
    __tablename__ = "forecast_features"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    route = Column(String)
    cargo_demand_index = Column(Float)
    vessel_supply_index = Column(Float)
    weather_risk_index = Column(Float)
    port_congestion_index = Column(Float)
    global_gdp_growth = Column(Float)

class VesselAvailability(Base):
    __tablename__ = "vessel_availability"
    id = Column(Integer, primary_key=True, index=True)
    vessel_name = Column(String)
    vessel_class = Column(String)
    open_position = Column(String)
    port = Column(String, index=True)
    source = Column(String)
    data_quality = Column(String)
