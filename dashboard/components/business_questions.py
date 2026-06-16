import streamlit as st
import pandas as pd
import plotly.express as px

def render_bq(df, color_map):
    st.markdown("<h1 style='color: #1E40AF;'>Strategic Business Insights</h1>", unsafe_allow_html=True)
    st.markdown("Analisis terarah untuk menjawab pertanyaan strategis mengenai faktor penentu performa akademik siswa.")
    st.divider()
    
    bq_select = st.selectbox("Pilih Pertanyaan Strategis (Business Question):", options=[
        "BQ1: Variabel penentu utama performa nilai ujian akhir?",
        "BQ2: Bagaimana dampak Keterlibatan Orang Tua terhadap nilai ujian?",
        "BQ3: Apakah motivasi belajar linier dengan alokasi waktu dan kehadiran?",
        "BQ4: Bagaimana profil finansial dan akses internet pada siswa High Risk?",
        "BQ5: Bagaimana pengaruh Kualitas Guru terhadap proporsi risiko akademik?",
        "BQ6: Kombinasi faktor dominan apa yang mencirikan siswa High Risk?"
    ])
    
    NUMERICAL_COLS = ['Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Scores', 'Tutoring_Sessions', 'Physical_Activity']
    st.markdown("<br>", unsafe_allow_html=True)

    if bq_select.startswith("BQ1"):
        st.markdown("#### Analisis Variabel Penentu Utama")
        st.info("**Pertanyaan:** Fitur-fitur apa saja yang memiliki korelasi tertinggi terhadap capaian Exam Score siswa?")
        corrs = df[NUMERICAL_COLS].corrwith(df['Exam_Score']).reset_index(name='Korelasi').sort_values(by='Korelasi', ascending=False)
        
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(corrs, x='Korelasi', y='index', orientation='h', title="Korelasi Numerik vs Exam Score", color='Korelasi', color_continuous_scale='Blues')
            fig1.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            cat_mean = df.groupby('Motivation_Level')['Exam_Score'].mean().reset_index()
            fig2 = px.bar(cat_mean, x='Motivation_Level', y='Exam_Score', title="Rata-rata Skor vs Motivasi", color='Motivation_Level', color_discrete_sequence=['#1E40AF'])
            fig2.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)
        st.success("**Strategic Insight:** *Attendance* dan *Hours Studied* adalah prediktor terkuat. Intervensi pada kehadiran akan memberikan dampak paling signifikan.")

    elif bq_select.startswith("BQ2"):
        st.markdown("#### Dampak Keterlibatan Orang Tua")
        st.info("**Pertanyaan:** Apakah tingkat Keterlibatan Orang Tua berdampak signifikan terhadap sebaran nilai ujian?")
        stats_involve = df.groupby('Parental_Involvement')['Exam_Score'].agg(['mean', 'std']).reset_index()
        
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(stats_involve, x='Parental_Involvement', y='mean', error_y='std', title="Mean Nilai Ujian ± Std Deviasi", color_discrete_sequence=['#1E40AF'])
            fig1.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.box(df, x='Parental_Involvement', y='Exam_Score', color='Parental_Involvement', title="Distribusi Nilai per Kategori")
            fig2.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)
        st.success("**Strategic Insight:** Keterlibatan orang tua yang tinggi secara konsisten menaikkan 'batas bawah' performa siswa.")

    elif bq_select.startswith("BQ3"):
        st.markdown("#### ⚡ Motivasi vs Kedisiplinan")
        st.info("**Pertanyaan:** Apakah motivasi belajar linier dengan alokasi waktu dan kehadiran?")
        m_hours = df.groupby('Motivation_Level')['Hours_Studied'].mean().reset_index()
        m_attend = df.groupby('Motivation_Level')['Attendance'].mean().reset_index()
        
        c1, c2 = st.columns(2)
        with c1:
            fig1 = px.bar(m_hours, x='Motivation_Level', y='Hours_Studied', title="Rata-rata Jam Belajar", color_discrete_sequence=['#1E40AF'])
            fig1.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig1, use_container_width=True)
        with c2:
            fig2 = px.bar(m_attend, x='Motivation_Level', y='Attendance', title="Rata-rata Kehadiran (%)", color_discrete_sequence=['#1E40AF'])
            fig2.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)
        st.success("**Strategic Insight:** Rendahnya motivasi adalah 'akar masalah' yang langsung bermanifestasi pada penurunan kehadiran dan jam belajar.")

    elif bq_select.startswith("BQ4"):
        st.markdown("#### Profil Sosio-Ekonomi High Risk")
        st.info("**Pertanyaan:** Bagaimana profil finansial dan akses internet pada siswa High Risk?")
        hr_df = df[df['Risk_Category'] == 'High']
        if len(hr_df) == 0:
            st.warning("⚠️ Tidak ada data siswa High Risk pada filter ini.")
        else:
            p_income = (hr_df['Family_Income'] == 'Low').mean() * 100
            p_internet = (hr_df['Internet_Access'] == 'No').mean() * 100
            bq4_data = pd.DataFrame({'Kondisi': ['Low Family Income', 'No Internet Access'], 'Persentase': [p_income, p_internet]})
            fig = px.bar(bq4_data, x='Persentase', y='Kondisi', orientation='h', text=bq4_data['Persentase'].apply(lambda x: f"{x:.1f}%"), 
                         title="Kondisi Lingkungan Kelompok High Risk", color_discrete_sequence=['#EF4444'], range_x=[0,100])
            fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig, use_container_width=True)
            st.success("**Strategic Insight:** Faktor ekonomi (*Low Income*) mendominasi kelompok berisiko, namun akses internet bukan lagi hambatan utama.")

    elif bq_select.startswith("BQ5"):
        st.markdown("#### Pengaruh Kualitas Pengajar")
        st.info("**Pertanyaan:** Bagaimana pengaruh Kualitas Guru terhadap proporsi risiko akademik?")
        prop_df = df.groupby(['Teacher_Quality', 'Risk_Category']).size().reset_index(name='Count')
        prop_df['Persentase'] = (prop_df['Count'] / prop_df.groupby('Teacher_Quality')['Count'].transform('sum') * 100).round(2)
        fig = px.bar(prop_df, x='Teacher_Quality', y='Persentase', color='Risk_Category', color_discrete_map=color_map, 
                     title="Proporsi Risiko per Kualitas Guru (%)")
        fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
        st.success("**Strategic Insight:** Guru berkualitas tinggi mampu mereduksi proporsi siswa di kategori *Medium* dan *High Risk* secara signifikan.")

    elif bq_select.startswith("BQ6"):
        st.markdown("#### Snapshot Karakteristik High Risk")
        st.info("**Pertanyaan:** Kombinasi faktor dominan apa yang mencirikan siswa High Risk?")
        hr_df = df[df['Risk_Category'] == 'High']
        if len(hr_df) == 0:
            st.warning("⚠️ Tidak ada data siswa High Risk.")
        else:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.plotly_chart(px.bar(hr_df['Motivation_Level'].value_counts(normalize=True).reset_index(name='p').assign(p=lambda x:x['p']*100), x='p', y='Motivation_Level', orientation='h', title='Motivasi (%)', color_discrete_sequence=['#EF4444']), use_container_width=True)
            with c2:
                st.plotly_chart(px.bar(hr_df['Parental_Involvement'].value_counts(normalize=True).reset_index(name='p').assign(p=lambda x:x['p']*100), x='p', y='Parental_Involvement', orientation='h', title='Keterlibatan OT (%)', color_discrete_sequence=['#EF4444']), use_container_width=True)
            with c3:
                st.plotly_chart(px.bar(hr_df['Family_Income'].value_counts(normalize=True).reset_index(name='p').assign(p=lambda x:x['p']*100), x='p', y='Family_Income', orientation='h', title='Pendapatan (%)', color_discrete_sequence=['#EF4444']), use_container_width=True)
            st.success("**Strategic Insight:** 'The High-Risk Trifecta': Motivasi Rendah + Ekonomi Rendah + Keterlibatan Orang Tua Minim.")