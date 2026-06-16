import streamlit as st
import plotly.express as px

def render_profiling(df_raw, color_map):
    st.markdown("<h1 style='color: #1E40AF;'>High-Risk Student Profiling</h1>", unsafe_allow_html=True)
    st.markdown("Analisis mendalam terhadap karakteristik siswa yang teridentifikasi dalam kategori risiko tinggi untuk perencanaan intervensi.")
    st.divider()
    
    # sidebar filter untuk fokus pada siswa high risk
    with st.sidebar:
        st.markdown("### Filter Profiling")
        hr_gender = st.selectbox("Gender:", ["All"] + list(df_raw['Gender'].unique()))
        hr_school = st.selectbox("Tipe Sekolah:", ["All"] + list(df_raw['School_Type'].unique()))
        hr_income = st.selectbox("Pendapatan Keluarga:", ["All"] + list(df_raw['Family_Income'].unique()))
    
    # filter data untuk siswa high risk
    df_hr = df_raw[df_raw['Risk_Category'] == 'High']
    if hr_gender != "All":
        df_hr = df_hr[df_hr['Gender'] == hr_gender]
    if hr_school != "All":
        df_hr = df_hr[df_hr['School_Type'] == hr_school]
    if hr_income != "All":
        df_hr = df_hr[df_hr['Family_Income'] == hr_income]
        
    total_hr_all = len(df_raw[df_raw['Risk_Category'] == 'High'])
    total_hr_filtered = len(df_hr)
    
    with st.container():
        st.markdown("### Ringkasan Profil")
        c_m1, c_m2 = st.columns(2)
        c_m1.metric("Siswa High Risk (Filtered)", f"{total_hr_filtered} siswa")
        c_m2.metric("Proporsi dari Total Kategori", f"{(total_hr_filtered/max(1, total_hr_all))*100:.2f}%")
    
    if total_hr_filtered == 0:
        st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih.")
        return

    st.divider()
    st.markdown("### Distribusi Fitur Utama (High Risk Only)")
    feats = ['Motivation_Level', 'Parental_Involvement', 'Family_Income', 'Teacher_Quality', 'Internet_Access', 'Peer_Influence']
    
    # Grid layout for charts
    for i in range(0, len(feats), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(feats):
                feat = feats[i + j]
                with cols[j]:
                    counts = df_hr[feat].value_counts().reset_index(name='Count')
                    fig = px.bar(counts, x=feat, y='Count', title=f"Distribusi {feat}", color_discrete_sequence=['#EF4444'])
                    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), height=300)
                    st.plotly_chart(fig, use_container_width=True)
            
    st.divider()
    st.markdown("### Daftar Prioritas Intervensi")
    display_cols = ['Risk_Category', 'Hours_Studied', 'Attendance', 'Previous_Scores', 'Motivation_Level', 'Parental_Involvement', 'Family_Income', 'Gender', 'School_Type']
    st.dataframe(df_hr[display_cols], use_container_width=True)
    
    csv_bytes = df_hr[display_cols].to_csv(index=False).encode('utf-8')
    st.download_button(label="Unduh Daftar Prioritas (CSV)", data=csv_bytes, file_name="Siswa_High_Risk_Prioritas.csv", mime="text/csv", use_container_width=True)