import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, root_mean_squared_error, mean_absolute_percentage_error
from database import engine

def fetch_data():
    query = "SELECT date, fuel_price, demand_index, rate FROM freight_rates ORDER BY date ASC"
    df = pd.read_sql(query, con=engine)
    df.dropna(inplace=True)
    return df

def feature_engineering(df):
    # Sort chronologically
    df = df.sort_values('date').reset_index(drop=True)
    
    # Lagged features
    df['rate_lag_1'] = df['rate'].shift(1)
    df['rate_lag_7'] = df['rate'].shift(7)
    df['fuel_lag_1'] = df['fuel_price'].shift(1)
    
    # Rolling features
    df['rate_rolling_7d'] = df['rate'].rolling(window=7).mean()
    
    # Drop rows with NaNs from rolling/lagging
    df = df.dropna().reset_index(drop=True)
    return df

def evaluate(y_true, y_pred, model_name):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = root_mean_squared_error(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    
    print(f"\n--- {model_name} Performance ---")
    print(f"MAE:  {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"MAPE: {mape:.2f}%")
    return {"model": model_name, "mae": round(mae,2), "rmse": round(rmse,2), "mape": round(mape,2)}

def train_models():
    print("Initiating REAL ML Pipeline...")
    df = fetch_data()
    if len(df) < 30:
        print("INSUFFICIENT HISTORICAL DATA. Aborting model train.")
        return
        
    df = feature_engineering(df)
    
    # Chronological Split (80/20)
    split_idx = int(len(df) * 0.8)
    train_df = df.iloc[:split_idx]
    test_df = df.iloc[split_idx:]
    
    features = ['fuel_price', 'demand_index', 'rate_lag_1', 'rate_lag_7', 'fuel_lag_1', 'rate_rolling_7d']
    target = 'rate'
    
    X_train, y_train = train_df[features], train_df[target]
    X_test, y_test = test_df[features], test_df[target]
    
    # BASELINE (Naive Predictor: Prev Day Rate)
    y_pred_naive = X_test['rate_lag_1']
    baseline_metrics = evaluate(y_test, y_pred_naive, "Naive Baseline (Lag 1)")
    
    # ML MODEL - Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    rf_metrics = evaluate(y_test, y_pred_rf, "Random Forest")
    
    # Improvement Validation
    improvement = ((baseline_metrics['mae'] - rf_metrics['mae']) / baseline_metrics['mae']) * 100
    print(f"\nModel Improvement over Baseline: {improvement:.2f}%")
    rf_metrics["improvement_vs_baseline"] = round(improvement, 2)
    
    # Save the model
    os.makedirs("models", exist_ok=True)
    with open("models/rf_model.pkl", "wb") as f:
        pickle.dump(rf_model, f)
        
    # Save metrics 
    with open("models/metrics.pkl", "wb") as f:
        pickle.dump({"random_forest": rf_metrics, "baseline": baseline_metrics}, f)
        
    print("\nModel trained and exported to models/rf_model.pkl")

if __name__ == "__main__":
    train_models()
