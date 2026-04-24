"""
Iron Ore Quality Predictor — Training Script
=============================================
Predicts % Silica Concentrate in a mining flotation plant.
Lower silica = higher iron ore purity.

Usage:
    python train_model.py
"""

import pandas as pd
import numpy as np
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import xgboost as xgb

# ── Config ──────────────────────────────────────────────────────────────────
DATA_PATH   = "data/MiningProcess_Flotation_Plant_Database.csv"
MODEL_DIR   = "models"
TARGET      = "% Silica Concentrate"
SAMPLE_SIZE = 100000
TEST_SIZE   = 0.2
RANDOM_STATE = 42

os.makedirs(MODEL_DIR, exist_ok=True)


def load_data(path, sample_size=SAMPLE_SIZE):
    print(f"Loading data from: {path}")
    df = pd.read_csv(path, decimal=',')
    print(f"Full dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
    df = df.drop(columns=['date'], errors='ignore')
    if sample_size and len(df) > sample_size:
        df = df.sample(n=sample_size, random_state=RANDOM_STATE)
        print(f"Sampled: {len(df):,} rows")
    return df


def preprocess(df, target):
    features = [c for c in df.columns if c != target]
    X = df[features].values
    y = df[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    scaler = StandardScaler()
    X_train_sc = scaler.fit_transform(X_train)
    X_test_sc  = scaler.transform(X_test)

    return X_train, X_test, X_train_sc, X_test_sc, y_train, y_test, scaler, features


def evaluate(name, y_true, y_pred):
    mae  = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2   = r2_score(y_true, y_pred)
    print(f"  {name:<20} → MAE: {mae:.4f} | RMSE: {rmse:.4f} | R²: {r2:.4f}")
    return {"mae": mae, "rmse": rmse, "r2": r2}


def main():
    print("=" * 55)
    print("    IRON ORE QUALITY PREDICTOR — TRAINING")
    print("=" * 55)

    # Load
    df = load_data(DATA_PATH)

    # Preprocess
    X_train, X_test, X_train_sc, X_test_sc, y_train, y_test, scaler, features = preprocess(df, TARGET)
    print(f"\nTrain: {X_train.shape[0]:,} | Test: {X_test.shape[0]:,}")
    print(f"Features: {len(features)}\n")

    # Train Random Forest
    print("Training Random Forest...")
    rf = RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=RANDOM_STATE)
    rf.fit(X_train, y_train)
    rf_metrics = evaluate("Random Forest", y_test, rf.predict(X_test))

    # Train XGBoost
    print("Training XGBoost...")
    xgb_model = xgb.XGBRegressor(
        n_estimators=200, learning_rate=0.05, max_depth=8,
        subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_STATE,
        tree_method='hist', verbosity=0
    )
    xgb_model.fit(X_train_sc, y_train)
    xgb_metrics = evaluate("XGBoost", y_test, xgb_model.predict(X_test_sc))

    # Save models
    print("\nSaving models...")
    joblib.dump(rf,        f"{MODEL_DIR}/random_forest_model.pkl")
    joblib.dump(xgb_model, f"{MODEL_DIR}/xgboost_model.pkl")
    joblib.dump(scaler,    f"{MODEL_DIR}/scaler.pkl")
    joblib.dump(features,  f"{MODEL_DIR}/feature_names.pkl")
    print(f"  ✅ Saved to ./{MODEL_DIR}/")

    best = "XGBoost" if xgb_metrics["r2"] > rf_metrics["r2"] else "Random Forest"
    print(f"\n🏆 Best Model: {best}")
    print("=" * 55)


if __name__ == "__main__":
    main()
