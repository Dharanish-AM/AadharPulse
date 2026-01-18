import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="Aadhaar Pulse Dashboard",
    page_icon="🇮🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- TITLE & INTRO ---
st.title("🇮🇳 Aadhaar Pulse: Ecosystem Analytics")
st.markdown("""
**Operational Intelligence for UIDAI** | Hackathon 2026 Submission
This dashboard provides real-time insights into Aadhaar enrolment trends, update volumes, and operational stress (UBI).
""")

# --- DATA LOADER ---
@st.cache_data
def load_data():
    # 1. Load Enrolment Data
    enrol_files = glob.glob("data/api_data_aadhar_enrolment/*.csv")
    if not enrol_files:
        st.error("No Enrolment Data found in data/api_data_aadhar_enrolment/")
        return None, None, None
    
    enrol_df = pd.concat([pd.read_csv(f) for f in enrol_files], ignore_index=True)
    # Parse Date
    enrol_df['date'] = pd.to_datetime(enrol_df['date'], format='%d-%m-%Y', errors='coerce')
    enrol_df['month'] = enrol_df['date'].dt.to_period('M').astype(str)
    # Calculate Total Enrolments
    enrol_df['total_enrolments'] = enrol_df['age_0_5'] + enrol_df['age_5_17'] + enrol_df['age_18_greater']

    # 2. Load Demographic Updates
    demo_files = glob.glob("data/api_data_aadhar_demographic/*.csv")
    demo_df = pd.concat([pd.read_csv(f) for f in demo_files], ignore_index=True)
    demo_df['date'] = pd.to_datetime(demo_df['date'], format='%d-%m-%Y', errors='coerce')
    demo_df['month'] = demo_df['date'].dt.to_period('M').astype(str)
    demo_df['total_demo_updates'] = demo_df['demo_age_5_17'] + demo_df['demo_age_17_']

    # 3. Load Biometric Updates
    bio_files = glob.glob("data/api_data_aadhar_biometric/*.csv")
    bio_df = pd.concat([pd.read_csv(f) for f in bio_files], ignore_index=True)
    bio_df['date'] = pd.to_datetime(bio_df['date'], format='%d-%m-%Y', errors='coerce')
    bio_df['month'] = bio_df['date'].dt.to_period('M').astype(str)
    bio_df['total_bio_updates'] = bio_df['bio_age_5_17'] + bio_df['bio_age_17_']

    # 4. Aggregations (State-Month Level)
    # Enrolment
    e_grp = enrol_df.groupby(['state', 'month'])['total_enrolments'].sum().reset_index()
    
    # Updates
    d_grp = demo_df.groupby(['state', 'month'])['total_demo_updates'].sum().reset_index()
    b_grp = bio_df.groupby(['state', 'month'])['total_bio_updates'].sum().reset_index()
    
    # Merge All
    merged = e_grp.merge(d_grp, on=['state', 'month'], how='left').merge(b_grp, on=['state', 'month'], how='left')
    merged.fillna(0, inplace=True)
    
    # Filter out invalid numeric states (e.g., '100000') found in raw data
    merged = merged[~merged['state'].astype(str).str.match(r'^\d+$')]
    
    
    # Calculated Fields
    merged['total_updates'] = merged['total_demo_updates'] + merged['total_bio_updates']
    merged['UBI'] = merged['total_updates'] / (merged['total_enrolments'] + 1) # Avoid div by zero
    
    return merged, enrol_df, d_grp # Return raw or intermediate as needed

# Load Data
df, raw_enrol, _ = load_data()

if df is None:
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filters")
all_states = sorted(df['state'].unique())
selected_states = st.sidebar.multiselect("Select State(s)", all_states, default=all_states[:5])

if not selected_states:
    filtered_df = df.copy()
else:
    filtered_df = df[df['state'].isin(selected_states)]

# --- KPI METRICS ---
col1, col2, col3, col4 = st.columns(4)
total_enrol = filtered_df['total_enrolments'].sum()
total_upd = filtered_df['total_updates'].sum()
avg_ubi = filtered_df['total_updates'].sum() / (filtered_df['total_enrolments'].sum() + 1)
top_state = filtered_df.groupby('state')['total_updates'].sum().idxmax()

col1.metric("Total Enrolments", f"{total_enrol:,}")
col2.metric("Total Updates", f"{total_upd:,}")
col3.metric("Avg Update Burden (UBI)", f"{avg_ubi:.2f}")
col4.metric("Highest Update State", top_state)

st.markdown("---")

# --- TABS ---
tab1, tab2, tab3 = st.tabs(["📈 Trends", "🗺️ Regional Analysis", "🚨 Hotspots"])

# TAB 1: TRENDS
with tab1:
    st.subheader("Monthly Ecosystem Activity")
    
    # Aggregate by month
    monthly = filtered_df.groupby('month')[['total_enrolments', 'total_updates']].sum().reset_index()
    monthly['month_dt'] = pd.to_datetime(monthly['month'])
    monthly = monthly.sort_values('month_dt')
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=monthly['month'], y=monthly['total_enrolments'], name='Enrolments', line=dict(color='#00CC96', width=4)))
    fig_trend.add_trace(go.Scatter(x=monthly['month'], y=monthly['total_updates'], name='Updates', line=dict(color='#EF553B', width=4)))
    fig_trend.update_layout(title="Enrolments vs Updates Over Time", template="plotly_dark", height=500)
    st.plotly_chart(fig_trend, use_container_width=True)

# TAB 2: REGIONAL
with tab2:
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Top States by Volume")
        # Top 10 States Aggregated
        top_states_enrol = filtered_df.groupby('state')['total_enrolments'].sum().nlargest(10).reset_index()
        fig_bar = px.bar(top_states_enrol, x='total_enrolments', y='state', orientation='h', 
                         title="Top 10 States by Enrolments", template="plotly_dark",
                         color='total_enrolments', color_continuous_scale='Viridis')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
    with col_b:
        st.subheader("Top States by Activity Type")
        # Updates vs Enrolments Scatter
        state_agg = filtered_df.groupby('state')[['total_enrolments', 'total_updates']].sum().reset_index()
        fig_scat = px.scatter(state_agg, x='total_enrolments', y='total_updates', size='total_updates', color='state',
                              title="Enrolment vs Update Correlation", template="plotly_dark", hover_name='state')
        st.plotly_chart(fig_scat, use_container_width=True)

# TAB 3: HOTSPOTS (UBI)
with tab3:
    st.subheader("Update Burden Index (UBI) Analysis")
    st.markdown("High UBI values (>4.0) indicate regions that function primarily as **maintenance hubs** rather than enrolment centers.")
    
    ubi_state = filtered_df.groupby('state')[['total_enrolments', 'total_updates']].sum().reset_index()
    ubi_state['UBI'] = ubi_state['total_updates'] / (ubi_state['total_enrolments'] + 1)
    ubi_state = ubi_state.sort_values('UBI', ascending=False).head(15)
    
    fig_ubi = px.bar(ubi_state, x='state', y='UBI', title="Top 15 States with Highest Operational Stress (UBI)",
                     template="plotly_dark", color='UBI', color_continuous_scale='Magma')
    st.plotly_chart(fig_ubi, use_container_width=True)
    
    # Anomaly Placeholder (Static for demo speed if needed, or calculated)
    st.info("💡 Insight: Specific districts in these states require dedicated Update Clinics.")

# --- FOOTER ---
st.markdown("---")
st.caption("Built with Streamlit for UIDAI Data Hackathon 2026")
