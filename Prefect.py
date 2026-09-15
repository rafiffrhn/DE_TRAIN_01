from prefect import task, flow
import pandas as pd
import numpy as np
import os
import duckdb
from datetime import timedelta 

@task(name="1_Transformasi_Data")
def transform_data():
    print("Menjalankan Transformasi...")
    df = pd.read_csv('data/raw/T1.csv')
    df.columns = ['timestamp', 'active_power_kw', 'wind_speed_ms', 'theoretical_power_kw', 'wind_direction_deg']
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d %m %Y %H:%M')
    df['year'] = df['timestamp'].dt.year
    df['month'] = df['timestamp'].dt.month
    df['day'] = df['timestamp'].dt.day
    df['hour'] = df['timestamp'].dt.hour
    
    df['active_power_kw'] = df['active_power_kw'].apply(lambda x: 0 if x < 0 else x)
    kondisi_rusak = (df['wind_speed_ms'] > 3.5) & (df['active_power_kw'] <= 0.1)
    df['turbine_status'] = np.where(kondisi_rusak, 'Maintenance/Error', 'Normal')
    
    output_path = 'data/processed/wind_turbine_cleaned.parquet'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)
    
    return output_path 

@task(name="2_Load_ke_Warehouse")
def load_data(parquet_path):
    print("Menjalankan Load ke DuckDB...")
    con = duckdb.connect('data/warehouse.db')
    con.execute("DROP TABLE IF EXISTS wind_turbine;")
    con.execute(f"CREATE TABLE wind_turbine AS SELECT * FROM '{parquet_path}';")
    con.close()

@flow(name="Wind Turbine ETL Pipeline")
def run_etl_pipeline():
    hasil_path = transform_data()
    load_data(hasil_path)

if __name__ == "__main__":

    run_etl_pipeline.serve(
        name="jadwal-turbin-harian",
        interval=timedelta(minutes=1) 
    )