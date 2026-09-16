# End-to-End Wind Turbine SCADA Pipeline & Machine Learning

## Deskripsi Proyek
Proyek ini adalah portofolio *Full-Stack Data* komprehensif yang menggabungkan bidang **Data Engineering** dan **Data Science**. Menggunakan dataset sensor IoT (*SCADA*) dari kincir angin, proyek ini merancang sistem *pipeline* data otomatis dari hulu ke hilir: mulai dari ekstraksi data mentah, pembersihan anomali, penyimpanan ke Data Warehouse, visualisasi Business Intelligence, hingga pengembangan model Machine Learning prediktif.

## Tech Stack & Tools
- **Bahasa Pemrograman:** Python 3
- **Data Engineering & ETL:** Prefect (Orchestration), DuckDB (Data Warehouse), PyArrow (Parquet)
- **Data Science & ML:** Scikit-Learn (Random Forest Regressor & Classifier), Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Power BI Desktop
- **Version Control:** Git & GitHub

## Struktur Repositori
```text
├── data/                    # Penyimpanan data (Processed / Parquet)
├── images/                  # Aset gambar untuk dokumentasi & dashboard
├── notebooks/               # Eksperimen & Pemodelan Data Science
│    ├── prediksi_daya.ipynb         # Model Regresi (Prediksi Active Power)
│    └── predictive_maintenance.ipynb # Model Klasifikasi (Deteksi Status Mesin)
├── Perfect.py               # Script orkestrasi ETL Pipeline otomatis
├── transform.py             # Logika transformasi & handling anomali
├── load.py                  # Load data ke DuckDB
└── README.md
```
## Part 1: Data Engineering (Automated Pipeline)
Pipeline diorkestrasi menggunakan Prefect dengan tahapan:
- **Extract & Clean:** Membaca data CSV, membersihkan nilai anomali (daya negatif), dan melakukan time-partitioning.
- **Feature Engineering:** Membuat kolom turbine_status (Normal vs Maintenance/Error) berdasarkan logika bisnis kecepatan angin dan daya.
- **Load:** Menyimpan data terstruktur ke format Parquet dan DuckDB secara otomatis.

## Part 2: Data Sciennce & Machine Learning
Di tahap ini, data bersih dieksplorasi lebih dalam menggunakan Jupyter Notebook di dalam folder notebooks/:
- **Model Regresi (regression_daya.ipynb):** Membangun RandomForestRegressor untuk memprediksi besarnya daya listrik (active_power_kw) berdasarkan kecepatan angin. Model ini sukses mencetak skor akurasi $R^2$ sebesar 96.15%.
- **Model Klasifikasi (classification_predmaintenance.ipynb):** Membangun RandomForestClassifier untuk mendeteksi status kerusakan mesin (Predictive Maintenance) serta menganalisis mitigasi Data Leakage untuk menguji performa model di dunia nyata.

## Visualisasi & Dashboard
- **Power BI:** Digunakan untuk monitoring performa operasional kincir angin secara interaktif.
- **Matplotlib & Seaborn:** Digunakan untuk evaluasi model Machine Learning (Scatter plot aktual vs prediksi dan analisis Feature Importance).

## Cara Menjalankan Proyek
1. **Clone Repositori ini
```bash
git clone https://github.com/rafiffrhn/end-to-end-data-pipeline-1.git
cd end-to-end-data-pipeline-1
```
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Jalankan pipeline Prefect atau buka Jupyter Notebook di dalam folder notebooks/ untuk melihat eksperimen model AI.
```bash
python -m prefect server start
```
Dashboard Prefect dapat diakses melalui http://127.0.0.1:4200

4. Jalankan Pipeline Automasi (Buka terminal kedua)
```bash
python Prefect.py
```
Script ini akan mengeksekusi pipeline (Transform & Load) secara otomatis berdasarkan jadwal yang sudah ditentukan pada code.
