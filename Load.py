import duckdb

def load_and_analyze():
    print("Menghubungkan ke Data Warehouse (DuckDB)...")
    
    # 1. BIKIN/KONEK KE DATABASE LOKAL
    con = duckdb.connect('data/warehouse.db')

    # 2. LOAD PARQUET KE DALAM TABEL (Tahap Load)
    print("Membuat tabel dari file Parquet...")
    
    con.execute("DROP TABLE IF EXISTS wind_turbine;")
    
    con.execute("""
        CREATE TABLE wind_turbine AS 
        SELECT * FROM 'data/processed/wind_turbine_cleaned.parquet';
    """)
    print("Data berhasil dimuat ke Data Warehouse!\n")

    # 3. JALANKAN ANALISIS SQL
    print("=== LAPORAN PERFORMA TURBIN ANGIN ===")
    
    print("1. Status Mesin:")
    status_query = """
        SELECT turbine_status, COUNT(*) as total_kejadian
        FROM wind_turbine
        GROUP BY turbine_status;
    """
    print(con.execute(status_query).fetchdf()) 
    print("-" * 40)

    # Query 2: Rata-rata daya yang dihasilkan per bulan
    print("2. Rata-rata Produksi Daya (kW) per Bulan:")
    monthly_query = """
        SELECT 
            year, 
            month, 
            ROUND(AVG(active_power_kw), 2) as rata_rata_daya_kw,
            ROUND(AVG(wind_speed_ms), 2) as rata_rata_kecepatan_angin
        FROM wind_turbine
        GROUP BY year, month
        ORDER BY year, month;
    """
    print(con.execute(monthly_query).fetchdf())

    con.close()

if __name__ == "__main__":
    load_and_analyze()