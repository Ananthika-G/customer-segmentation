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

elif page == "RFM Deep Dive":
    st.title("🔍 RFM Deep Dive")
    st.markdown("Explore R, F, M dimensions interactively.")
    st.markdown("---")

    st.subheader("Interactive 3D RFM scatter")
    fig_3d = px.scatter_3d(
        rfm, x='Recency', y='Frequency', z='Monetary',
        color='Segment', size_max=8, opacity=0.65,
        color_discrete_sequence=px.colors.qualitative.Set2,
        hover_data=['Customer ID','RFM_Score'])
    fig_3d.update_layout(height=550, margin=dict(l=0,r=0,t=30,b=0))
    st.plotly_chart(fig_3d, use_container_width=True)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("RFM score distribution")
        fig_rfm = px.histogram(rfm, x='RFM_Total', nbins=13,
                               color_discrete_sequence=['#7c3aed'])
        fig_rfm.update_layout(height=320)
        st.plotly_chart(fig_rfm, use_container_width=True)

    with col_r:
        st.subheader("Avg RFM scores by segment")
        rfm_avg = rfm.groupby('Segment')[['R_Score','F_Score','M_Score']].mean().round(2)
        fig_heat = px.imshow(rfm_avg, color_continuous_scale='RdYlGn',
                             aspect='auto', text_auto=True)
        fig_heat.update_layout(height=320)
        st.plotly_chart(fig_heat, use_container_width=True)

    st.subheader("Top 20 customers by RFM score")
    top20 = rfm.nlargest(20,'RFM_Total')[
        ['Customer ID','Recency','Frequency','Monetary','RFM_Score','Segment']]
    st.dataframe(top20.reset_index(drop=True), use_container_width=True)
elif page == "Retention Strategies":
    st.title("💡 Retention Strategies")
    st.markdown("Data-driven recommendations for each segment.")
    st.markdown("---")

    col1,col2,col3 = st.columns(3)
    critical = strategies[strategies['Priority']=='Critical']
    high = strategies[strategies['Priority']=='High']
    col1.metric("Critical Priority", len(critical), delta="Immediate action")
    col2.metric("High Priority", len(high))
    col3.metric("Total Strategies", len(strategies))

    st.markdown("---")
    st.subheader("Strategy table")

    priority_filter = st.multiselect("Filter by priority:",
        options=strategies['Priority'].unique().tolist(),
        default=strategies['Priority'].unique().tolist())
    filtered_strat = strategies[strategies['Priority'].isin(priority_filter)]
    st.dataframe(filtered_strat[['Segment','Priority','Strategy',
        'Actions','Channel','Expected_Impact','Estimated_ROI']],
        use_container_width=True, height=280)

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        st.subheader("Revenue at risk by segment")
        seg_rev = rfm.groupby('Segment')['Monetary'].sum().reset_index()
        seg_rev = seg_rev.merge(strategies[['Segment','Priority']], on='Segment', how='left')
        color_map = {'Critical':'#a32d2d','High':'#d97706',
                     'Medium':'#185fa5','Low':'#6b7280'}
        fig_rev = px.bar(seg_rev.sort_values('Monetary', ascending=True),
                         x='Monetary', y='Segment', orientation='h',
                         color='Priority', color_discrete_map=color_map)
        fig_rev.update_layout(height=350)
        fig_rev.update_xaxes(tickprefix='£', tickformat=',.0f')
        st.plotly_chart(fig_rev, use_container_width=True)

    with col_r:
        st.subheader("At-Risk customers detail")
        at_risk = rfm[rfm['Segment']=='At-Risk'].sort_values('Recency', ascending=False)
        st.markdown(f"**{len(at_risk)} customers at risk**")
        st.dataframe(at_risk[['Customer ID','Recency','Frequency',
            'Monetary','RFM_Score']].head(20).reset_index(drop=True),
            use_container_width=True, height=300)

    st.markdown("---")
    st.subheader("📥 Download at-risk customer list")
    at_risk_csv = rfm[rfm['Segment']=='At-Risk'].to_csv(index=False)
    st.download_button(label="Download At-Risk customers CSV",
        data=at_risk_csv, file_name="at_risk_customers.csv", mime="text/csv")

        # app.py structure:
# 1. Imports
# 2. st.set_page_config(...)
# 3. @st.cache_data → load_data()
# 4. Sidebar navigation
# 5. if page == "Overview": ...
# 6. elif page == "Segment Analysis": ...
# 7. elif page == "RFM Deep Dive": ...
# 8. elif page == "Retention Strategies": ...

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

# Fallback for Streamlit Cloud
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join(os.getcwd(), 'data', 'processed')

@st.cache_data
def load_data():
    rfm        = pd.read_csv(os.path.join(DATA_DIR, 'rfm_clustered.csv'))
    strategies = pd.read_csv(os.path.join(DATA_DIR, 'retention_strategies.csv'))
    return rfm, strategies