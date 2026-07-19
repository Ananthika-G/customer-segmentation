import streamlit as st
import pandas as pd, numpy as np
import plotly.express as px
import plotly.graph_objects as go
import warnings;
import os
warnings.filterwarnings('ignore')


st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

@st.cache_data
def load_data():
    rfm = pd.read_csv(os.path.join(DATA_DIR, 'rfm_clustered.csv'))
    strategies = pd.read_csv(os.path.join(DATA_DIR, 'retention_strategies.csv'))
    return rfm, strategies

rfm, strategies = load_data()

st.sidebar.title("📊 Navigation")
page = st.sidebar.radio("Go to",
    ["Overview","Segment Analysis","RFM Deep Dive","Retention Strategies"])

st.sidebar.markdown("---")
st.sidebar.markdown("**Project:** Customer Segmentation")
st.sidebar.markdown("**Author:** Ananthika G")

if page == "Overview":
    st.title("📊 Customer Segmentation & Retention Analysis")
    st.markdown("Analysing **3,921 UK customers** from Online Retail II (2009-2011)")
    st.markdown("---")

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Total Customers", f"{len(rfm):,}")
    col2.metric("Total Revenue", f"£{rfm['Monetary'].sum()/1e6:.1f}M")
    col3.metric("Avg Customer Spend", f"£{rfm['Monetary'].mean():,.0f}")
    col4.metric("Segments Identified", rfm['Segment'].nunique())

    st.markdown("---")
    col_left, col_right = st.columns(2)

    with col_left:
        st.subheader("Customer segment distribution")
        seg_counts = rfm['Segment'].value_counts().reset_index()
        seg_counts.columns = ['Segment','Count']
        fig_pie = px.pie(seg_counts, names='Segment', values='Count',
                         color_discrete_sequence=px.colors.qualitative.Set2,
                         hole=0.4)
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(height=380, showlegend=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        st.subheader("Revenue by segment")
        seg_rev = rfm.groupby('Segment')['Monetary'].sum().reset_index()
        seg_rev = seg_rev.sort_values('Monetary', ascending=True)
        fig_bar = px.bar(seg_rev, x='Monetary', y='Segment',
                         orientation='h', color='Monetary',
                         color_continuous_scale='Teal',
                         labels={'Monetary':'Total Revenue (£)','Segment':''})
        fig_bar.update_layout(height=380, coloraxis_showscale=False)
        fig_bar.update_xaxes(tickprefix='£', tickformat=',.0f')
        st.plotly_chart(fig_bar, use_container_width=True)

elif page == "Segment Analysis":
    st.title("🎯 Segment Analysis")

    selected_seg = st.selectbox(
        "Select a segment to explore:",
        ["All"] + sorted(rfm['Segment'].unique().tolist()))

    filtered = rfm if selected_seg=="All" else rfm[rfm['Segment']==selected_seg]

    col1,col2,col3,col4 = st.columns(4)
    col1.metric("Customers",  f"{len(filtered):,}")
    col2.metric("Avg Recency", f"{filtered['Recency'].mean():.0f} days")
    col3.metric("Avg Orders",  f"{filtered['Frequency'].mean():.1f}")
    col4.metric("Avg Spend",   f"£{filtered['Monetary'].mean():,.0f}")

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Recency vs Frequency")
        fig_sc = px.scatter(filtered, x='Recency', y='Frequency',
                            color='Segment', size='Monetary',
                            hover_data=['Customer ID','Monetary'],
                            color_discrete_sequence=px.colors.qualitative.Set2)
        fig_sc.update_layout(height=380)
        st.plotly_chart(fig_sc, use_container_width=True)

    with col_r:
        st.subheader("Spend distribution")
        spend_cap = filtered[filtered['Monetary'] < filtered['Monetary'].quantile(0.95)]
        fig_hist = px.histogram(spend_cap, x='Monetary', nbins=40,
                                color_discrete_sequence=['#0369a1'])
        fig_hist.update_layout(height=380)
        st.plotly_chart(fig_hist, use_container_width=True)

    st.subheader("Segment data table")
    st.dataframe(
        filtered[['Customer ID','Recency','Frequency','Monetary','Segment','RFM_Score']]
        .sort_values('Monetary', ascending=False).head(50).reset_index(drop=True),
        use_container_width=True)