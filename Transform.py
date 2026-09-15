import pandas as pd
import numpy as np
import os

def run_transformation():
    print("Memulai proses transformasi data...")

    # 1. LOAD DATA MENTAH
    df = pd.read_csv('data/raw/T1.csv')

    # 2. STANDARISASI NAMA KOLOM
    df.columns = [
        'timestamp', 
        'active_power_kw', 
        'wind_speed_ms', 
        'theoretical_power_kw', 
        'wind_direction_deg'
    ]

    # 3. TRANSFORMASI WAKTU (Time Partitioning)
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d %m %Y %H:%M')

    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour

    # 4. PENANGANAN ANOMALI (Handling Anomalies)
    df['active_power_kw'] = df['active_power_kw'].apply(lambda x: 0 if x < 0 else x)

    # 5. DATA QUALITY CHECK (Membuat Kolom Status)
    kondisi_rusak = (df['wind_speed_ms'] > 3.5) & (df['active_power_kw'] <= 0.1)
    df['turbine_status'] = np.where(kondisi_rusak, 'Maintenance/Error', 'Normal')

    # 6. SIMPAN DATA BERSIH (Load to Parquet)
    output_path = 'data/processed/wind_turbine_cleaned.parquet'
    
    df.to_parquet(output_path, index=False)

    print(f"Sukses! Data bersih berhasil disimpan di: {output_path}")
    print("\nPreview 5 baris pertama data bersih:")
    print(df.head())

if __name__ == "__main__":
    run_transformation()