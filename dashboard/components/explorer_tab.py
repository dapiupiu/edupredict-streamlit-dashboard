import streamlit as st

def render_explorer(df_raw):
    st.markdown("<h1 style='color: #1E40AF;'>Data Explorer</h1>", unsafe_allow_html=True)
    st.markdown("Gunakan alat ini untuk menyaring, menyortir, dan mendalami baris data siswa secara spesifik.")
    st.divider()
    
    # sidebar filter
    with st.sidebar:
        st.markdown("### Filter Eksplorasi")
        exp_risk = st.multiselect("Risk Category:", options=['High', 'Medium', 'Low'], default=['High', 'Medium', 'Low'])
        exp_gender = st.selectbox("Gender:", ["All"] + list(df_raw['Gender'].unique()))
        exp_school = st.selectbox("School Type:", ["All"] + list(df_raw['School_Type'].unique()))
    
    # filter data
    df_exp = df_raw[df_raw['Risk_Category'].isin(exp_risk)]
    if exp_gender != "All":
        df_exp = df_exp[df_exp['Gender'] == exp_gender]
    if exp_school != "All":
        df_exp = df_exp[df_exp['School_Type'] == exp_school]
        
    st.info(f"**Hasil Pencarian:** Ditemukan {len(df_exp)} baris data.")
    
    if len(df_exp) == 0:
        st.warning("⚠️ Tidak ada data yang sesuai dengan kombinasi kriteria pencarian.")
        return

    # highlight anomali (High Risk)
    def highlight_high_risk(row):
        return ['background-color: #FEE2E2' if row['Risk_Category'] == 'High' else '' for _ in row]
        
    st.markdown("#### Preview Data")
    st.dataframe(df_exp.style.apply(highlight_high_risk, axis=1), use_container_width=True, height=500)
    
    st.divider()
    csv_bytes = df_exp.to_csv(index=False).encode('utf-8')
    st.download_button(label="Unduh Hasil Eksplorasi (CSV)", data=csv_bytes, file_name="EduPredict_Filtered_Explorer.csv", mime="text/csv", use_container_width=True)