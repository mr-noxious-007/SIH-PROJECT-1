-- FILE: db/schema.sql

CREATE TABLE VesselTypes (
    id SERIAL PRIMARY KEY,
    vessel_type VARCHAR(50) NOT NULL,
    typical_capacity_tons INT,
    typical_draft_meters DECIMAL(5,2),
    typical_loa_meters DECIMAL(6,2),
    typical_beam_meters DECIMAL(5,2),
    daily_operating_cost_usd INT,
    fuel_consumption_tons_per_day DECIMAL(5,2),
    description TEXT
);

CREATE TABLE PortSpecifications (
    id SERIAL PRIMARY KEY,
    port_name VARCHAR(100) NOT NULL,
    country VARCHAR(50) DEFAULT 'India',
    region VARCHAR(50) DEFAULT 'East Coast',
    max_draft_meters DECIMAL(5,2),
    max_loa_meters DECIMAL(6,2),
    max_beam_meters DECIMAL(5,2),
    cargo_handling_rate_tons_per_day INT,
    berthing_capacity INT,
    current_congestion_percent INT DEFAULT 0,
    average_turnaround_days DECIMAL(5,1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE FreightRates (
    id SERIAL PRIMARY KEY,
    vessel_type VARCHAR(50),
    origin_port VARCHAR(100),
    destination_port VARCHAR(100),
    rate_usd_per_ton DECIMAL(10,2),
    date DATE,
    trend VARCHAR(20),
    predicted_rate_7day DECIMAL(10,2),
    predicted_rate_30day DECIMAL(10,2),
    confidence_score INT,
    source VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE FreightHistory (
    id SERIAL PRIMARY KEY,
    vessel_type VARCHAR(50),
    origin VARCHAR(100),
    destination VARCHAR(100),
    rate_usd DECIMAL(10,2),
    year INT,
    month INT,
    seasonal_factor DECIMAL(3,2)
);

CREATE TABLE UserQueries (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(100),
    cargo_type VARCHAR(50),
    cargo_volume_tons INT,
    origin_port VARCHAR(100),
    destination_port VARCHAR(100),
    preferred_vessel_type VARCHAR(50),
    budget_usd INT,
    contract_duration_days INT,
    status VARCHAR(50) DEFAULT 'New',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Recommendations (
    id SERIAL PRIMARY KEY,
    query_id INT REFERENCES UserQueries(id),
    recommended_vessel_type VARCHAR(50),
    predicted_rate_low_usd DECIMAL(10,2),
    predicted_rate_high_usd DECIMAL(10,2),
    best_entry_window VARCHAR(100),
    estimated_savings_percent DECIMAL(5,2),
    estimated_savings_usd INT,
    port_compatibility_score INT,
    draft_check VARCHAR(50),
    loa_check VARCHAR(50),
    beam_check VARCHAR(50),
    estimated_idle_days INT,
    total_voyage_cost_usd INT,
    vs_spot_price_usd INT,
    confidence_percent INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_freight_rates_vessel_dest_date ON FreightRates(vessel_type, destination_port, date);
