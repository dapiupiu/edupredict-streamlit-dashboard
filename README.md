# 🎓 EduPredict AI: Early Warning Detection System for Academic

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

**EduPredict AI** adalah platform analitik cerdas yang dirancang untuk mendeteksi dini risiko performa akademik siswa. Dengan mengintegrasikan data historis dan teknik *Machine Learning*, sistem ini memberikan wawasan mendalam bagi pendidik untuk melakukan intervensi tepat waktu sebelum siswa mengalami kegagalan akademik seperti penurunan nilai, prestasi rendah, tidak naik kelas hingga drop out (putus sekolah).

---

## 📌 Deskripsi Proyek

Proyek ini berfokus pada analisis faktor-faktor yang mempengaruhi keberhasilan akademik siswa, mulai dari aspek internal (seperti motivasi dan jam belajar) hingga aspek eksternal (seperti keterlibatan orang tua dan latar belakang ekonomi). Sistem ini mengkategorikan siswa ke dalam tiga tingkat risiko: **Low**, **Medium**, dan **High Risk**.

Tujuan utama dari proyek ini adalah:
- **Identifikasi Dini:** Menemukan siswa yang membutuhkan perhatian khusus berdasarkan profil data mereka.
- **Analisis Prediktif:** Memahami variabel kunci yang mendorong risiko kegagalan akademik.
- **Intervensi Cerdas:** Memberikan saran tindakan yang personal menggunakan teknologi LLM.
- **Pengambilan Keputusan:** Memberikan rekomendasi berbasis data bagi pihak sekolah atau institusi pendidikan.

---

## 🚀 Fitur Utama

Dashboard EduPredict AI terbagi menjadi beberapa modul fungsional:

1.  **Overview (Ringkasan Eksekutif):** Visualisasi metrik utama populasi siswa, distribusi kategori risiko, dan ringkasan kondisi akademik secara keseluruhan.
2.  **Exploratory Data Analysis (EDA):** Analisis mendalam mengenai hubungan antar variabel (misalnya: korelasi antara jam belajar dengan nilai ujian).
3.  **Business Questions:** Jawaban atas pertanyaan strategis terkait pengaruh keterlibatan orang tua, motivasi, dan akses sumber daya terhadap performa siswa.
4.  **Profil High Risk:** Fokus khusus pada karakteristik siswa kategori risiko tinggi untuk memahami pola perilaku dan hambatan yang mereka hadapi.
5.  **Uji Komparatif:** Membandingkan metrik tertentu (seperti kehadiran) antar kelompok kategori risiko menggunakan visualisasi distribusi.
6.  **Data Explorer:** Antarmuka interaktif untuk melihat, mencari, dan memfilter data mentah yang digunakan dalam analisis.
7.  **Prediksi Risiko & Intervensi AI:** Simulator interaktif menggunakan Neural Network untuk memprediksi risiko secara real-time, lengkap dengan **Rekomendasi Intervensi otomatis berbasis model Groq AI dan Railway API**.

---

## 📂 Struktur Proyek

```text
edupredict-ai/
├── dashboard/               # Kode utama aplikasi Streamlit
│   ├── assets/              # Gambar dan aset statis lainnya
│   ├── components/          # Modul modular untuk setiap halaman dashboard
│   │   ├── business_questions.py
│   │   ├── comparative_tab.py
│   │   ├── eda_tab.py
│   │   ├── explorer_tab.py
│   │   ├── overview_tab.py
│   │   ├── predict_tab.py
│   │   └── profiling_tab.py
│   └── dashboard.py         # Entry point aplikasi
├── data/                    # Penyimpanan dataset (Diabaikan oleh Git)
│   ├── processed/           # Data yang sudah dibersihkan
│   └── raw/                 # Data mentah
├── models/                  # File model ML (e.g., .pkl, .keras, .joblib)
├── notebooks/               # Dokumentasi proses DS/ML 
│   ├── edupredict_clean.ipynb
│   └── edupredict_train.ipynb
├── .streamlit/              # Konfigurasi Streamlit (Tema dan Server)
│   ├── config.toml          
├── .gitignore               # Konfigurasi file yang diabaikan Git
├── README.md                # Dokumentasi proyek
└── requirements.txt         # Daftar dependensi library
```

---

## 🛠️ Panduan Menjalankan Program

Ikuti langkah-langkah berikut untuk menjalankan dashboard di lingkungan lokal Anda:

### 1. Prasyarat
- Python 3.9 atau versi yang lebih baru terinstal.
- Disarankan menggunakan virtual environment (venv).

### 2. Instalasi
Clone repositori ini dan instal dependensi yang diperlukan:
```bash
# Clone repositori
git clone https://github.com/dapiupiu/edupredict-ai.git
cd edupredict-ai

# Buat virtual environment
python -m venv .venv

# Aktivasi venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Instal dependensi
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard
Jalankan perintah berikut dari direktori root proyek:
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi akan terbuka secara otomatis di browser Anda di alamat `http://localhost:8501`.

---

## 📈 Saran Pengembangan Kedepan

Untuk meningkatkan akurasi dan kegunaan sistem, beberapa aspek berikut dapat dikembangkan lebih lanjut:

- **Integrasi Database:** Menghubungkan dashboard langsung ke Sistem Informasi Akademik (SIAKAD) untuk data *real-time*.
- **Model Advanced:** Eksperimen dengan algoritma Deep Learning atau Ensemble Methods (XGBoost/LightGBM) untuk meningkatkan presisi pada kelas minoritas (*High Risk*).
- **Sistem Notifikasi:** Integrasi dengan Email atau WhatsApp Gateway untuk mengirim peringatan (alert) otomatis kepada wali kelas atau orang tua.
- **Fitur Prediksi Nilai Ujian:** Menambahkan prediksi nilai ujian kemudian mengelompokkan jenis risikonya agar sistem lebih informatif dan mendukung pengambilan keputusan yang lebih akurat.
- **Multilingual Support:** Dukungan bahasa tambahan untuk dashboard dan intervensi AI.

---

## 📝 Catatan Tambahan
*Dataset yang digunakan dalam demo ini telah dienkripsi atau menggunakan dummy data jika file `.csv` asli tidak ditemukan di folder `data/processed/`, untuk menjaga privasi informasi siswa.*

---
**© 2026 EduPredict AI Project | CC26-PSU080.**