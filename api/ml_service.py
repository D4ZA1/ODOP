
import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor


def process_file(file_path, target_date=None, use_saved_models=True):

    print(f"[DEBUG] Processing file: {file_path}")
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    print("[DEBUG] Parsing and engineering features...")
    df['Arrival_Date'] = pd.to_datetime(df['Arrival_Date'], dayfirst=True)
    df.sort_values("Arrival_Date", inplace=True)
    df['Modal_Price'] = df['Modal_Price'].ffill()

    df['Month'] = df['Arrival_Date'].dt.month
    df['Week'] = df['Arrival_Date'].dt.isocalendar().week.astype(int)
    df['Day'] = df['Arrival_Date'].dt.day
    df['DayOfWeek'] = df['Arrival_Date'].dt.dayofweek
    df['Is_Weekend'] = df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
    df['Price_Spread'] = df['Max_Price'] - df['Min_Price']
    df['Price_Variation'] = df['Max_Price'] - df['Modal_Price']
    df['Lag_1'] = df['Modal_Price'].shift(1)
    df['Lag_2'] = df['Modal_Price'].shift(2)
    df['Lag_3'] = df['Modal_Price'].shift(3)
    df['Roll_Mean_3'] = df['Modal_Price'].rolling(3).mean()
    df['Roll_Std_3'] = df['Modal_Price'].rolling(3).std()
    df.dropna(inplace=True)

    features = ['Min_Price', 'Max_Price', 'Month', 'Week', 'Day', 'DayOfWeek',
                'Is_Weekend', 'Price_Spread', 'Price_Variation',
                'Lag_1', 'Lag_2', 'Lag_3', 'Roll_Mean_3', 'Roll_Std_3']
    target = 'Modal_Price'

    scaler_X = MinMaxScaler()
    X = df[features]
    y = df[[target]]
    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y = MinMaxScaler().fit_transform(y).flatten()

    split = int(len(X_scaled) * 0.8)
    if split == 0:
        split = 1
    X_train, X_test = X_scaled[:split], X_scaled[split:]
    y_train, y_test = y_scaled[:split], y_scaled[split:]

    model_name = os.path.splitext(os.path.basename(file_path))[0]
    model_dir = "data/saved_models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, f"{model_name}.joblib")

    use_cached = use_saved_models and os.path.exists(model_path)
    if use_cached:
        print(f"[DEBUG] Loading cached model from {model_path}")
        model = load(model_path)
    else:
        print("[DEBUG] Training new model...")
        model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
        model.fit(X_train, y_train)
        dump(model, model_path)
        print(f"[DEBUG] Model saved to {model_path}")

    if len(X_test) > 0:
        y_pred_scaled = model.predict(X_test)
        y_pred = scaler_y.reshape(-1, 1)[split:]
        y_pred = scaler_y[:len(y_pred_scaled)].reshape(-1, 1)
        y_test_orig = scaler_y[:len(y_pred_scaled)].reshape(-1, 1)

        mae = mean_absolute_error(y_test_orig, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test_orig, y_pred))
        r2 = r2_score(y_test_orig, y_pred)
    else:
        print("[WARN] No test set available for evaluation.")
        mae, rmse, r2 = 0, 0, 0

    max_price = np.max(df[target])
    normalized_mae_score = 1 - (mae / max_price)
    normalized_rmse_score = 1 - (rmse / max_price)

    forecast = None
    if target_date:
        print("[DEBUG] Forecasting for target date...")
        last_date = df['Arrival_Date'].iloc[-1]
        future_df = df.copy()
        current_date = last_date + timedelta(days=1)
        target_date = pd.to_datetime(target_date)

        while current_date <= target_date:
            new_row = {
                'Arrival_Date': current_date,
                'Min_Price': future_df['Modal_Price'].iloc[-1] * 0.9,
                'Max_Price': future_df['Modal_Price'].iloc[-1] * 1.1,
            }
            temp_df = pd.concat([future_df, pd.DataFrame([new_row])], ignore_index=True)
            temp_df.loc[temp_df.index[-1], 'Modal_Price'] = np.nan
            temp_df['Month'] = temp_df['Arrival_Date'].dt.month
            temp_df['Week'] = temp_df['Arrival_Date'].dt.isocalendar().week.astype(int)
            temp_df['Day'] = temp_df['Arrival_Date'].dt.day
            temp_df['DayOfWeek'] = temp_df['Arrival_Date'].dt.dayofweek
            temp_df['Is_Weekend'] = temp_df['DayOfWeek'].apply(lambda x: 1 if x >= 5 else 0)
            temp_df['Price_Spread'] = temp_df['Max_Price'] - temp_df['Min_Price']
            temp_df['Price_Variation'] = temp_df['Max_Price'] - temp_df['Modal_Price']
            temp_df['Lag_1'] = temp_df['Modal_Price'].shift(1)
            temp_df['Lag_2'] = temp_df['Modal_Price'].shift(2)
            temp_df['Lag_3'] = temp_df['Modal_Price'].shift(3)
            temp_df['Roll_Mean_3'] = temp_df['Modal_Price'].rolling(3).mean()
            temp_df['Roll_Std_3'] = temp_df['Modal_Price'].rolling(3).std()

            last_row = temp_df.iloc[-1][features]

            if last_row.isnull().any():
                predicted_price = future_df['Modal_Price'].iloc[-1]
            else:
                X_future = scaler_X.transform([last_row])
                pred_scaled = model.predict(X_future)
                predicted_price = scaler_y.reshape(-1, 1)[0][0]

            temp_df.at[temp_df.index[-1], 'Modal_Price'] = predicted_price
            future_df = temp_df.copy()
            current_date += timedelta(days=1)

        final_price = future_df[future_df['Arrival_Date'] == target_date]['Modal_Price'].values[0]
        avg_last_7_days = df.tail(7)['Modal_Price'].mean()

        diff_percent = ((final_price - avg_last_7_days) / avg_last_7_days) * 100
        if diff_percent < -20:
            label = "Extremely Underpriced"
        elif diff_percent < -15:
            label = "Very Heavily Underpriced"
        elif diff_percent < -10:
            label = "Heavily Underpriced"
        elif diff_percent < -5:
            label = "Moderately Underpriced"
        elif diff_percent < 5:
            label = "Fairly Priced"
        elif diff_percent < 10:
            label = "Moderately Overpriced"
        elif diff_percent < 15:
            label = "Heavily Overpriced"
        elif diff_percent < 20:
            label = "Very Heavily Overpriced"
        else:
            label = "Extremely Overpriced"

        timeline = future_df[['Arrival_Date', 'Modal_Price']].tail(30)
        forecast = {
            "Predicted Price on {}".format(target_date.date()): round(final_price, 2),
            "7-Day Avg Before Forecast": round(avg_last_7_days, 2),
            "Price Status": label,
            "Price Timeline": [
                {"date": row['Arrival_Date'].strftime("%Y-%m-%d"), "price": round(row['Modal_Price'], 2)}
                for _, row in timeline.iterrows()
            ]
        }

    return mae, rmse, r2, normalized_mae_score, normalized_rmse_score, forecast

def get_model_evaluation_results(dataset_path="dataset"):
    os.makedirs(dataset_path, exist_ok=True)
    results = []
    for file in os.listdir(dataset_path):
        if file.endswith(('.csv', '.xlsx')):
            if not file.lower().startswith("apple"):
                continue
            print(f"[DEBUG] Evaluating model for file: {file}")
            try:
                path = os.path.join(dataset_path, file)
                mae, rmse, r2, nmae, nrmse, _ = process_file(path, use_saved_models=True)
                results.append({
                    "File": file,
                    "MAE": round(mae, 2),
                    "RMSE": round(rmse, 2),
                    "R2 Score": round(r2, 4),
                    "Normalized MAE Score": round(nmae, 4),
                    "Normalized RMSE Score": round(nrmse, 4)
                })
            except Exception as e:
                print(f"[ERROR] Failed to evaluate {file}: {e}")
                results.append({"File": file, "Error": str(e)})
    return sorted(results, key=lambda x: -x.get("Normalized RMSE Score", 0))

def get_future_price_predictions(target_date="2026-04-05", dataset_path="dataset", use_saved_models=True):
    os.makedirs(dataset_path, exist_ok=True)
    forecasts = []
    for file in os.listdir(dataset_path):
        if file.endswith(('.csv', '.xlsx')):
            if not file.lower().startswith("apple"):
                continue
            print(f"[DEBUG] Forecasting future prices for: {file}")
            try:
                path = os.path.join(dataset_path, file)
                _, _, _, _, _, forecast = process_file(path, target_date=target_date, use_saved_models=use_saved_models)
                if forecast:
                    forecast_result = {"File": file}
                    forecast_result.update(forecast)
                    forecasts.append(forecast_result)
            except Exception as e:
                print(f"[ERROR] Forecast failed for {file}: {e}")
                forecasts.append({"File": file, "Error": str(e)})
    return forecasts
