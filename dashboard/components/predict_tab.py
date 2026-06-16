import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import tensorflow as tf
import requests

def get_genai_insight(input_data, risk_category, confidence, predicted_score=0.0):
    """Fungsi untuk mengambil insight dari API Railway GenAI berdasarkan input data siswa"""
    RAILWAY_URL = "https://edupredictaiprod.up.railway.app/api/v1/analyze/recommendations"

    payload = {
        "student_id": "STU-Realtime",
        "features": input_data,
        "prediction": {
            "risk_category": risk_category,
            "confidence": float(confidence),
            "predicted_exam_score": float(predicted_score)
        }
    }

    try:
        # kirim data input ke API Railway
        response = requests.post(RAILWAY_URL, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            recs = result.get('recommendations', [])
            if recs:
                formatted_recs = []
                for r in recs:
                    title = r.get('title', 'Rekomendasi')
                    desc = r.get('description', '')
                    action = r.get('action', '')
                    formatted_recs.append(f"### {title}\n{desc}\n\n**Aksi:** {action}")
                return "\n\n---\n\n".join(formatted_recs)
            return "Tidak ada rekomendasi yang diberikan oleh AI."
        else:
            return f"Error API: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Gagal terhubung ke Gen AI: {str(e)}"

@st.cache_resource
def load_ml_artifacts():
    """Memuat model keras dan semua object pkl pendukung menggunakan caching resource"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(current_dir, "..", "..", "models")
    
    artifacts = {}
    try:
        # load model Keras (.keras) dengan caching resource untuk efisiensi
        artifacts['model'] = tf.keras.models.load_model(os.path.join(model_dir, "edupredict_multioutput.keras"))
        
        # load semua objek pkl pendukung: scaler, label encoders, feature columns, dan risk map
        with open(os.path.join(model_dir, "scaler.pkl"), "rb") as f:
            artifacts['scaler'] = pickle.load(f)
        with open(os.path.join(model_dir, "label_encoders.pkl"), "rb") as f:
            artifacts['label_encoders'] = pickle.load(f)
        with open(os.path.join(model_dir, "feature_cols.pkl"), "rb") as f:
            artifacts['feature_cols'] = pickle.load(f)
        with open(os.path.join(model_dir, "risk_map.pkl"), "rb") as f:
            artifacts['risk_map'] = pickle.load(f)
            
        artifacts['status'] = "Success"
    except Exception as e:
        artifacts['status'] = f"Error: {str(e)}"
        
    return artifacts

# konfigurasi batas distribusi data pelatihan untuk input clamping dan OOD detection
TRAINING_BOUNDS = {
    'Attendance':      (60, 100),
    'Hours_Studied':   (4,  36),
    'Previous_Scores': (50, 100),
    'Sleep_Hours':     (4,  10),
    'Tutoring_Sessions': (0, 7),
    'Physical_Activity': (0, 6),
}

def clamp_input(input_dict):
    """Membatasi nilai input ke dalam range yang pernah dilihat model saat training (input clamping)"""
    clamped = input_dict.copy()
    for col, (lo, hi) in TRAINING_BOUNDS.items():
        if col in clamped:
            clamped[col] = max(lo, min(hi, clamped[col]))
    return clamped

def render_predict(color_map):
    st.markdown("<h1 style='color: #1E40AF;'>Real-Time Risk Prediction</h1>", unsafe_allow_html=True)
    st.markdown("Masukkan indikator performa harian siswa untuk mengestimasikan kategori risiko akademis secara instan menggunakan AI.")
    st.divider()

    # memuat model ML dan objek pendukung
    artifacts = load_ml_artifacts()
    
    if "Error" in artifacts['status']:
        st.error("❌ Gagal memuat artifak model ML.")
        st.info("Detail: " + artifacts['status'])
        return
        
    feature_cols = artifacts['feature_cols']
    label_encoders = artifacts['label_encoders']
    scaler = artifacts['scaler']
    model = artifacts['model']
    risk_map = artifacts['risk_map']
    
    if isinstance(list(risk_map.keys())[0], str):
        label_to_idx = risk_map
        idx_to_label = {v: k for k, v in risk_map.items()}
    else:
        idx_to_label = risk_map
        label_to_idx = {v: k for k, v in risk_map.items()}

    # form input parameter siswa
    with st.form("prediction_form", border=True):
        st.markdown("### Parameter Input Siswa")
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("<p style='font-weight: 600; color: #1E40AF; border-bottom: 2px solid #E2E8F0; padding-bottom: 5px;'>Akademis & Kedisiplinan</p>", unsafe_allow_html=True)
            hours_studied = st.slider("Jam Belajar Per Minggu:", 1, 50, 15)
            attendance = st.slider("Persentase Kehadiran (%):", 0, 100, 85)
            previous_scores = st.slider("Nilai Rapor Sebelumnya:", 0, 100, 75)
            tutoring_sessions = st.number_input("Jumlah Sesi Bimbingan:", min_value=0, max_value=20, value=1, step=1)
            sleep_hours = st.slider("Rata-rata Jam Tidur:", 3, 12, 7)
            physical_activity = st.slider("Frekuensi Olahraga:", 0, 7, 3)

        with c2:
            st.markdown("<p style='font-weight: 600; color: #1E40AF; border-bottom: 2px solid #E2E8F0; padding-bottom: 5px;'>Psikososial & Lingkungan</p>", unsafe_allow_html=True)
            motivation_level = st.selectbox("Tingkat Motivasi:", options=list(label_encoders['Motivation_Level'].classes_), index=1)
            parental_involvement = st.selectbox("Keterlibatan Orang Tua:", options=list(label_encoders['Parental_Involvement'].classes_), index=1)
            access_resources = st.selectbox("Akses Fasilitas Belajar:", options=list(label_encoders['Access_to_Resources'].classes_), index=1)
            teacher_quality = st.selectbox("Kualitas Pengajar:", options=list(label_encoders['Teacher_Quality'].classes_), index=1)
            family_income = st.selectbox("Pendapatan Keluarga:", options=list(label_encoders['Family_Income'].classes_), index=1)
            parental_edu = st.selectbox("Pendidikan Orang Tua:", options=list(label_encoders['Parental_Education_Level'].classes_), index=1)
            peer_influence = st.selectbox("Pengaruh Teman Sebaya:", options=list(label_encoders['Peer_Influence'].classes_), index=1)
            internet_access = st.radio("Akses Internet:", options=list(label_encoders['Internet_Access'].classes_), index=1, horizontal=True)

        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("🚀 Hitung Estimasi Risiko Akademik", use_container_width=True)

    if submit_btn:
        input_data = {
            'Hours_Studied': hours_studied,
            'Attendance': attendance,
            'Parental_Involvement': parental_involvement,
            'Access_to_Resources': access_resources,
            'Sleep_Hours': sleep_hours,
            'Previous_Scores': previous_scores,
            'Motivation_Level': motivation_level,
            'Internet_Access': internet_access,
            'Tutoring_Sessions': tutoring_sessions,
            'Family_Income': family_income,
            'Teacher_Quality': teacher_quality,
            'Peer_Influence': peer_influence,
            'Physical_Activity': physical_activity,
            'Parental_Education_Level': parental_edu
        }
        
        clamped_data = clamp_input(input_data)
        input_df = pd.DataFrame([clamped_data])
        input_df = input_df[feature_cols]
        
        cat_cols_to_encode = ['Parental_Involvement', 'Access_to_Resources', 'Motivation_Level', 'Internet_Access', 'Family_Income', 'Teacher_Quality', 'Peer_Influence', 'Parental_Education_Level']
        for col in cat_cols_to_encode:
            encoder = label_encoders[col]
            input_df[col] = encoder.transform(input_df[col])
            
        input_scaled = scaler.transform(input_df)
        preds = model.predict(input_scaled)
        
        if isinstance(preds, list):
            risk_pred_array = [p for p in preds if p.shape[1] == 3][0]
        else:
            risk_pred_array = preds
            
        pred_idx = np.argmax(risk_pred_array[0])
        probabilities = risk_pred_array[0]
        final_risk_label = idx_to_label.get(pred_idx, "Unknown")

        with st.spinner("Menganalisis data dengan AI..."):
            ai_insight = get_genai_insight(
                input_data,
                risk_category=final_risk_label,
                confidence=probabilities[pred_idx]
            )

        st.divider()
        st.markdown("### Hasil Analisis Kecerdasan Buatan")
        
        chosen_color = color_map.get(final_risk_label, "#7f8c8d")
        
        st.markdown(
            f"""
            <div style="background: linear-gradient(135deg, {chosen_color} 0%, {chosen_color}CC 100%); padding:30px; border-radius:16px; text-align:center; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);">
                <h1 style="color:white; margin:0; font-size: 2.5rem; font-weight: 800; letter-spacing: 1px;">{final_risk_label.upper()} RISK</h1>
                <p style="color:white; margin:10px 0 0 0; font-size:18px; opacity: 0.9;">Tingkat kerentanan akademik siswa berada di kelas risiko {final_risk_label}.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
            c_p1, c_p2, c_p3 = st.columns(3)
            c_p1.metric("Low Risk Confidence", f"{probabilities[label_to_idx['Low']]*100:.2f}%")
            c_p2.metric("Medium Risk Confidence", f"{probabilities[label_to_idx['Medium']]*100:.2f}%")
            c_p3.metric("High Risk Confidence", f"{probabilities[label_to_idx['High']]*100:.2f}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("Lihat Rekomendasi Intervensi AI", expanded=True):
            st.info(ai_insight)