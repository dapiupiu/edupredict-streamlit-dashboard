import streamlit as st
import pandas as pd
import numpy as np
import os

# Impor komponen modular dari folder components
from components.overview_tab import render_overview
from components.eda_tab import render_eda
from components.business_questions import render_bq
from components.profiling_tab import render_profiling
from components.comparative_tab import render_comparative
from components.explorer_tab import render_explorer
from components.predict_tab import render_predict

# Konfigurasi Halaman Utama
current_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(current_dir, "assets", "logo.png")

st.set_page_config(
    layout="wide", 
    page_title="EduPredict AI", 
    page_icon=logo_path
)

st.markdown("""
<style>
    /* Impor Font Modern */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Styling Container Utama */
    .main {
        background-color: #FFFFFF;
    }

    /* Styling Card dan Kontainer */
    div[data-testid="stMetric"] {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        transition: transform 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    /* Styling Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #F0F4F8;
        border-right: 1px solid #E2E8F0;
    }
    section[data-testid="stSidebar"] .st-emotion-cache-6qob1r {
        background-color: transparent;
    }

    /* Tombol Radio Sidebar */
    div[data-testid="stSidebarNav"] {
        padding-top: 20px;
    }

    /* Heading Sidebar */
    .sidebar-title {
        color: #1E40AF;
        font-weight: 700;
        font-size: 1.5rem;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Custom Card Style for general containers */
    .custom-card {
        background-color: white;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        margin-bottom: 20px;
    }

    /* Styling Divider */
    hr {
        margin-top: 1rem;
        margin-bottom: 1rem;
        border: 0;
        border-top: 1px solid #E2E8F0;
    }

    /* Style for Buttons */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    /* Plotly Chart Container */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

COLOR_MAP = {'High': '#EF4444', 'Medium': '#F59E0B', 'Low': '#10B981'}

@st.cache_data
def load_historical_data():
    """Memuat data historis untuk visualisasi"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "processed", "edupredict_cleaned.csv")
    
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    else:
        # Jika file tidak ditemukan, buat dummy data untuk keperluan pengembangan dan demo
        np.random.seed(42)
        n_rows = 6607
        dummy_data = {
            'Hours_Studied': np.random.randint(1, 30, n_rows),
            'Attendance': np.random.randint(50, 100, n_rows),
            'Sleep_Hours': np.random.randint(4, 10, n_rows),
            'Previous_Scores': np.random.randint(40, 100, n_rows),
            'Tutoring_Sessions': np.random.randint(0, 5, n_rows),
            'Physical_Activity': np.random.randint(0, 7, n_rows),
            'Parental_Involvement': np.random.choice(['Low', 'Medium', 'High'], n_rows),
            'Access_to_Resources': np.random.choice(['Low', 'Medium', 'High'], n_rows),
            'Motivation_Level': np.random.choice(['Low', 'Medium', 'High'], n_rows),
            'Internet_Access': np.random.choice(['Yes', 'No'], n_rows, p=[0.85, 0.15]),
            'Family_Income': np.random.choice(['Low', 'Medium', 'High'], n_rows, p=[0.4, 0.4, 0.2]),
            'Teacher_Quality': np.random.choice(['Low', 'Medium', 'High'], n_rows),
            'Peer_Influence': np.random.choice(['Negative', 'Neutral', 'Positive'], n_rows),
            'Parental_Education_Level': np.random.choice(['High School', 'Bachelor', 'Master'], n_rows),
            'Gender': np.random.choice(['Male', 'Female'], n_rows),
            'School_Type': np.random.choice(['Public', 'Private'], n_rows),
            'Learning_Disabilities': np.random.choice(['Yes', 'No'], n_rows, p=[0.05, 0.95]),
            'Distance_from_Home': np.random.choice(['Near', 'Moderate', 'Far'], n_rows),
            'Extracurricular_Activities': np.random.choice(['Yes', 'No'], n_rows),
            'Exam_Score': np.random.randint(30, 100, n_rows),
            'Risk_Category': np.random.choice(['High', 'Medium', 'Low'], n_rows, p=[0.01, 0.83, 0.16])
        }
        df_dummy = pd.DataFrame(dummy_data)
        df_dummy.loc[df_dummy['Risk_Category'] == 'High', 'Family_Income'] = np.random.choice(['Low', 'Medium'], size=len(df_dummy[df_dummy['Risk_Category'] == 'High']), p=[0.55, 0.45])
        df_dummy.loc[df_dummy['Risk_Category'] == 'High', 'Motivation_Level'] = np.random.choice(['Low', 'Medium'], size=len(df_dummy[df_dummy['Risk_Category'] == 'High']), p=[0.53, 0.47])
        return df_dummy

df_raw = load_historical_data()

# sidebar navigasi utama
with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(logo_path, use_container_width=True)
    
    st.markdown("<div class='sidebar-title'>EduPredict AI</div>", unsafe_allow_html=True)
    st.divider()
    
    page = st.radio(
        "Pilih Halaman Navigasi:",
        [
            "Overview", 
            "Exploratory Data Analysis", 
            "Business Questions", 
            "Profil High Risk", 
            "Uji Komparatif (Attendance)", 
            "Data Explorer",
            "Prediksi Risiko Real-Time"
        ]
    )
    st.divider()

# filter global untuk halaman Overview, EDA, dan Business Questions
if page in ["Overview", "Exploratory Data Analysis", "Business Questions"]:
    with st.sidebar:
        st.markdown("### Filter Global")
        global_risk = st.multiselect(
            "Kategori Risiko:", options=['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low']
        )
        global_school = st.selectbox(
            "Tipe Sekolah:", options=["All"] + list(df_raw['School_Type'].unique()), index=0
        )
        
        df_filtered = df_raw[df_raw['Risk_Category'].isin(global_risk)]
        if global_school != "All":
            df_filtered = df_filtered[df_filtered['School_Type'] == global_school]
        
        # Metric di sidebar dipercantik dengan container kustom
        st.info(f"**Data Aktif:** {len(df_filtered)} / {len(df_raw)} siswa")
    
    if len(df_filtered) == 0:
        st.title(page)
        st.warning("⚠️ Tidak ada data historis yang sesuai dengan kombinasi filter global.")
        st.stop()
else:
    df_filtered = df_raw

# render halaman sesuai pilihan navigasi
if page == "Overview":
    render_overview(df_filtered, COLOR_MAP)
elif page == "Exploratory Data Analysis":
    render_eda(df_filtered, COLOR_MAP)
elif page == "Business Questions":
    render_bq(df_filtered, COLOR_MAP)
elif page == "Profil High Risk":
    render_profiling(df_raw, COLOR_MAP)
elif page == "Uji Komparatif (Attendance)":
    render_comparative(df_raw)
elif page == "Data Explorer":
    render_explorer(df_raw)
elif page == "Prediksi Risiko Real-Time":
    render_predict(COLOR_MAP)