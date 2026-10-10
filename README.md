# EduPredict AI: Dashboard Analitik Risiko Akademik Siswa

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

**[🔗 Buka Dashboard Live](https://edupredict-dashboard-cc26psu080.streamlit.app/)** · [Repositori Proyek (fork)](https://github.com/dapiupiu/edupredict-project) · [Repositori Tim](https://github.com/raelkertiaa/edupredict) · [Dokumentasi Data Science](https://github.com/raelkertiaa/edupredict/tree/data-science)

Dashboard **Streamlit** untuk menjelajahi faktor-faktor yang memengaruhi performa akademik siswa dan mengelompokkan siswa ke dalam tiga tingkat risiko (**Low**, **Medium**, **High**). Dashboard ini adalah bagian analitik dari **EduPredict AI**, Capstone Project *Coding Camp 2026 powered by DBS Foundation* (Team ID CC26-PSU080).

> **Peran saya:** Project Lead dan Data Scientist (data wrangling, EDA, business questions, dan dashboard ini). Model prediksi dikerjakan tim AI, dan aplikasi web utama dikerjakan tim Full-Stack.

---

## Deskripsi Proyek

Penurunan performa akademik sering terlambat terdeteksi karena data kehadiran, kebiasaan belajar, motivasi, dan kondisi sosial-ekonomi tidak dipantau secara terpadu. Dashboard ini membantu pendidik melihat faktor-faktor tersebut dalam satu tempat, dari aspek internal (motivasi, jam belajar, kehadiran) hingga eksternal (keterlibatan orang tua, latar belakang ekonomi).

Tujuan utama:
- **Identifikasi Dini:** menemukan kelompok siswa yang membutuhkan perhatian khusus berdasarkan profil datanya.
- **Analisis Faktor:** memahami variabel yang paling berkaitan dengan risiko akademik.
- **Pengambilan Keputusan:** memberi dasar berbasis data bagi sekolah untuk merancang intervensi.

**Dataset:** [Student Performance Factors (Kaggle)](https://www.kaggle.com/datasets/lainguyn123/student-performance-factors), 6.607 baris dan 20 kolom. Ini dataset publik, bukan data siswa sebenarnya. Variabel target `Risk_Category` diturunkan dari `Exam_Score` (High < 60, Medium 60 – 70, Low > 70).

---

## Temuan Utama

- **Perilaku belajar adalah sinyal terkuat:** korelasi dengan `Exam_Score` untuk `Attendance` **0,58** dan `Hours_Studied` **0,45**.
- **Keterlibatan orang tua berhubungan positif tetapi moderat:** rata-rata nilai High 68,09 · Medium 67,10 · Low 66,36.
- **Motivasi tidak menunjukkan hubungan kuat** dengan jam belajar maupun kehadiran pada dataset ini.
- **Profil siswa High Risk bersifat multidimensi:** 52,9% bermotivasi rendah, 54,4% berasal dari keluarga berpendapatan rendah, dan 85,3% memiliki keterlibatan orang tua rendah-menengah.

> Temuan bersifat asosiatif pada dataset ini dan tidak membuktikan hubungan sebab-akibat.

---

## Fitur Utama

Dashboard terbagi menjadi beberapa modul:

1.  **Overview:** metrik utama populasi siswa, distribusi kategori risiko, dan ringkasan kondisi akademik.
2.  **Exploratory Data Analysis (EDA):** hubungan antar variabel (mis. jam belajar dengan nilai ujian).
3.  **Business Questions:** jawaban atas pertanyaan strategis tentang pengaruh keterlibatan orang tua, motivasi, dan akses sumber daya terhadap performa siswa.
4.  **Profil High Risk:** karakteristik siswa risiko tinggi untuk memahami pola dan hambatan mereka.
5.  **Uji Komparatif:** perbandingan metrik (mis. kehadiran) antar kategori risiko dengan visualisasi distribusi.
6.  **Data Explorer:** antarmuka interaktif untuk melihat, mencari, dan memfilter data yang dipakai dalam analisis.
7.  **Prediksi Risiko:** simulator interaktif yang memanfaatkan model Neural Network dan layanan AI dari tim AI/Full-Stack untuk memperkirakan kategori risiko dari input pengguna.

---

## Struktur Proyek

```text
edupredict-streamlit-dashboard/
├── dashboard/               # Kode utama aplikasi Streamlit
│   ├── assets/              # Gambar dan aset statis lainnya
│   ├── components/          # Modul untuk setiap halaman dashboard
│   │   ├── business_questions.py
│   │   ├── comparative_tab.py
│   │   ├── eda_tab.py
│   │   ├── explorer_tab.py
│   │   ├── overview_tab.py
│   │   ├── predict_tab.py
│   │   └── profiling_tab.py
│   └── dashboard.py         # Entry point aplikasi
├── data/                    # Dataset (diabaikan oleh Git)
│   ├── processed/           # Data yang sudah dibersihkan
│   └── raw/                 # Data mentah
├── models/                  # File model ML (.pkl, .keras, .joblib)
├── notebooks/               # Dokumentasi proses DS/ML
│   ├── edupredict_clean.ipynb
│   └── edupredict_train.ipynb
├── .streamlit/              # Konfigurasi Streamlit (tema dan server)
│   └── config.toml
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Panduan Menjalankan Program

### 1. Prasyarat
- Python 3.9 atau lebih baru.
- Disarankan memakai virtual environment (venv).

### 2. Instalasi
```bash
# Clone repositori
git clone https://github.com/dapiupiu/edupredict-streamlit-dashboard.git
cd edupredict-streamlit-dashboard

# Buat dan aktifkan virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# Instal dependensi
pip install -r requirements.txt
```

### 3. Menjalankan Dashboard
```bash
streamlit run dashboard/dashboard.py
```
Aplikasi terbuka di `http://localhost:8501`.

---

## Saran Pengembangan

- **Integrasi Database:** menghubungkan dashboard ke Sistem Informasi Akademik (SIAKAD) untuk data real-time.
- **Model Lanjutan:** mencoba Ensemble Methods (XGBoost/LightGBM) untuk meningkatkan presisi pada kelas minoritas (*High Risk*).
- **Sistem Notifikasi:** peringatan otomatis lewat email atau WhatsApp kepada wali kelas atau orang tua.
- **Multilingual Support:** dukungan bahasa tambahan untuk dashboard.

---

## Catatan Data

Folder `data/` tidak disertakan di Git. Letakkan dataset bersih di `data/processed/`. Jika file CSV tidak ditemukan, dashboard memakai **data dummy** sebagai cadangan, sehingga angka yang tampil pada kondisi tersebut tidak mewakili hasil analisis di atas.

---

**© 2026 EduPredict AI Project | Team CC26-PSU080**
