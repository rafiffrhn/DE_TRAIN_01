# 🌬️ Wind Turbine SCADA ETL Pipeline

## 📌 Deskripsi Proyek
Proyek ini adalah *End-to-End Data Engineering Pipeline* yang memproses data sensor IoT (*SCADA*) dari kincir angin (Wind Turbine). Pipeline ini dirancang untuk menarik data mentah, melakukan transformasi dan *data cleaning* secara otomatis, menyimpannya ke dalam sistem Data Warehouse lokal, dan memvisualisasikan hasilnya untuk keperluan *Business Intelligence*.

Tujuan utama dari proyek ini adalah mengidentifikasi performa mesin dan membedakan kapan kincir angin beroperasi secara **Normal** dan kapan mengalami **Error/Maintenance** berdasarkan anomali data daya dan kecepatan angin.

## 🛠️ Tech Stack & Tools
- **Bahasa Pemrograman:** Python
- **Data Processing:** Pandas, NumPy
- **Format Penyimpanan:** Parquet (PyArrow)
- **Data Warehouse:** DuckDB
- **Orkestrasi & Automasi:** Prefect
- **Data Visualization:** Power BI Desktop

## 🗄️ Dataset
Data yang digunakan berasal dari Kaggle: [Wind Turbine SCADA Dataset](https://www.kaggle.com/datasets/berkerisen/wind-turbine-scada-dataset). Dataset ini berisi log sensor yang direkam setiap 10 menit, mencakup:
- `Date/Time`: Waktu pencatatan.
- `LV ActivePower (kW)`: Daya yang dihasilkan.
- `Wind Speed (m/s)`: Kecepatan angin.
- `Theoretical_Power_Curve (KWh)`: Daya teoritis.
- `Wind Direction (°)`: Arah angin.

## ⚙️ Arsitektur Data Pipeline (ETL)
Pipeline ini diorkestrasi menggunakan **Prefect** dengan tahapan berikut:

1. **Extract (E):** Membaca data mentah (*raw data*) berformat CSV.
2. **Transform (T):**
   - **Standarisasi Kolom:** Mengubah nama kolom menjadi format *snake_case* agar *SQL-friendly*.
   - **Time Partitioning:** Memecah kolom *timestamp* menjadi kolom `year`, `month`, `day`, dan `hour`.
   - **Handling Anomalies:** Mengubah nilai daya (Active Power) negatif menjadi 0.
   - **Business Logic (Feature Engineering):** Membuat kolom baru `turbine_status`. Jika kecepatan angin > 3.5 m/s tetapi daya yang dihasilkan <= 0.1 kW, maka status ditandai sebagai `Maintenance/Error`. Jika tidak, ditandai `Normal`.
   - **Optimasi Penyimpanan:** Mengonversi data hasil olahan menjadi format **Parquet**.
3. **Load (L):** Membuat tabel baru dan memuat data Parquet ke dalam *Data Warehouse* lokal menggunakan **DuckDB**.

## 📊 Hasil Visualisasi (Dashboard)
Data bersih yang tersimpan dihubungkan secara langsung ke **Power BI** untuk membuat *dashboard* monitoring interaktif.

![Power BI Dashboard](https://drive.google.com/file/d/15ZW2_hPG3bdV1e1ZmPgurbOCVwbrxhKx/view?usp=sharing)

![Prefect Orchestration](https://drive.google.com/file/d/1neh1XFl5h8Z0Up9BZDR6sou6SnYfr0zq/view?usp=drive_link)

## 🚀 Cara Menjalankan Proyek Ini (How to Run)

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/rafiffrhn/DE_TRAIN_01.git
   cd DE_TRAIN_01

2. **Install Requirements**
   ```bash
   pip install -r requirements.txt

3. **Siapkan Raw Dataset:**
  Buat folder data/raw/ di dalam direktori proyek, lalu unduh dan masukkan file T1.csv dari Kaggle ke dalam folder tersebut

4. **Nyalakan Prefect Server (Buka terminal pertama)**
   ```bash
   python -m prefect server start

4. **Jalankan Pipeline Automasi (Buka terminal kedua):**
   ```bash
   python Perfect.py
