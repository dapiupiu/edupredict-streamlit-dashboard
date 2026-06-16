import streamlit as st
import plotly.express as px

def render_eda(df, color_map):
    st.markdown("<h1 style='color: #1E40AF;'>Exploratory Data Analysis</h1>", unsafe_allow_html=True)
    st.markdown("Eksplorasi mendalam distribusi fitur numerik, kategorikal, dan pola hubungan variabel untuk memahami faktor risiko.")
    st.divider()
    
    tab_num, tab_cat, tab_corr, tab_scatter = st.tabs(["Numerik", "Kategorikal", "Korelasi", "Scatterplot"])
    
    NUMERICAL_COLS = ['Hours_Studied', 'Attendance', 'Sleep_Hours', 'Previous_Scores', 'Tutoring_Sessions', 'Physical_Activity']
    CATEGORICAL_FEATURES = ['Parental_Involvement', 'Access_to_Resources', 'Motivation_Level', 'Internet_Access', 'Family_Income', 'Teacher_Quality', 'Peer_Influence', 'Parental_Education_Level', 'Gender', 'School_Type', 'Learning_Disabilities', 'Distance_from_Home', 'Extracurricular_Activities']

    with tab_num:
        st.markdown("### Analisis Distribusi Numerik")
        col_sel, _ = st.columns([1, 1])
        with col_sel:
            selected_num = st.selectbox("Pilih Fitur Numerik:", NUMERICAL_COLS, key="num_sel")
        
        fig_hist = px.histogram(df, x=selected_num, color="Risk_Category", marginal="box", opacity=0.7, barmode="overlay",
                                title=f"Distribusi Fitur: {selected_num}", color_discrete_map=color_map)
        fig_hist.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with tab_cat:
        st.markdown("### Analisis Distribusi Kategorikal")
        col_sel, _ = st.columns([1, 1])
        with col_sel:
            selected_cat = st.selectbox("Pilih Fitur Kategorikal:", CATEGORICAL_FEATURES, key="cat_sel")
            
        cat_counts = df.groupby([selected_cat, 'Risk_Category']).size().reset_index(name='Jumlah')
        fig_cat = px.bar(cat_counts, x=selected_cat, y='Jumlah', color='Risk_Category', barmode='group',
                         title=f"Segmentasi Berdasarkan {selected_cat}", color_discrete_map=color_map)
        fig_cat.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with tab_corr:
        st.markdown("### Matriks Korelasi Fitur")
        corr_cols = NUMERICAL_COLS + ['Exam_Score']
        corr_matrix = df[corr_cols].corr()
        fig_heat = px.imshow(corr_matrix, text_auto=True, color_continuous_scale='RdBu_r', 
                            title='Korelasi Pearson (Asosiasi terhadap Exam Score)')
        fig_heat.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with tab_scatter:
        st.markdown("### Eksplorasi Hubungan Variabel")
        c1, c2 = st.columns(2)
        with c1:
            scat_x = st.selectbox("Sumbu X:", options=NUMERICAL_COLS, index=1, key="scat_x")
        with c2:
            scat_y = st.selectbox("Sumbu Y:", options=NUMERICAL_COLS + ['Exam_Score'], index=0, key="scat_y")
            
        fig_scat = px.scatter(df, x=scat_x, y=scat_y, color='Risk_Category', opacity=0.6,
                              title=f"Scatterplot: {scat_x} vs {scat_y}", color_discrete_map=color_map)
        fig_scat.update_layout(margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig_scat, use_container_width=True)