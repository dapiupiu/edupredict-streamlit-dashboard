import streamlit as st
import plotly.express as px

def render_overview(df, color_map):
    st.markdown("<h1 style='color: #1E40AF;'>Executive Overview</h1>", unsafe_allow_html=True)
    st.markdown("Sistem *Early Warning Detection* berbasis data historis dan integrasi AI untuk deteksi dini risiko performa akademik siswa.")
    st.divider()
    
    # kalkulasi metrik utama
    total_siswa = len(df)
    high_count = len(df[df['Risk_Category'] == 'High'])
    med_count = len(df[df['Risk_Category'] == 'Medium'])
    low_count = len(df[df['Risk_Category'] == 'Low'])
    
    with st.container():
        st.markdown("### Key Performance Indicators")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Siswa", f"{total_siswa:,}")
        col2.metric("High Risk", f"{high_count:,}", delta=f"{(high_count/max(1, total_siswa))*100:.1f}%", delta_color="inverse")
        col3.metric("Medium Risk", f"{med_count:,}", delta=f"{(med_count/max(1, total_siswa))*100:.1f}%", delta_color="off")
        col4.metric("Low Risk", f"{low_count:,}", delta=f"{(low_count/max(1, total_siswa))*100:.1f}%", delta_color="normal")
    
    st.divider()

    with st.container():
        st.markdown("### Distribusi Kategori Risiko")
        c1, c2 = st.columns(2)
        
        with c1:
            risk_dist = df['Risk_Category'].value_counts().reset_index()
            risk_dist.columns = ['Risk_Category', 'Count']
            fig_donut = px.pie(risk_dist, names='Risk_Category', values='Count', hole=0.5,
                               title='Proporsi Kategori Risiko', color='Risk_Category', color_discrete_map=color_map)
            fig_donut.update_layout(margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig_donut, use_container_width=True)
            
        with c2:
            risk_dist['Persentase'] = (risk_dist['Count'] / risk_dist['Count'].sum() * 100).round(2)
            fig_bar = px.bar(risk_dist, x='Risk_Category', y='Count', text=risk_dist.apply(lambda r: f"{r['Count']} ({r['Persentase']}%)", axis=1),
                             title='Volume Siswa per Kategori', color='Risk_Category', color_discrete_map=color_map)
            fig_bar.update_layout(yaxis_title="Jumlah Siswa", xaxis_title="", margin=dict(t=40, b=0, l=0, r=0))
            st.plotly_chart(fig_bar, use_container_width=True)
            
    st.divider()
    
    col_info, col_alert = st.columns([2, 1])
    with col_info:
        st.markdown("### Ringkasan Analisis")
        st.info(f"Berdasarkan filter aktif, terdapat **{high_count} siswa ({(high_count/max(1, total_siswa))*100:.1f}%)** yang tergolong dalam kategori **High Risk**.")
    with col_alert:
        st.markdown("### Catatan Penting")
        st.warning("Kelas **High Risk** berjumlah minoritas namun membutuhkan intervensi paling intensif.")