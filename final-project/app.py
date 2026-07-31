import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Global Health & Demographics Dashboard",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
    <style>
    .main { background-color: #FFFFFF; }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Color constants (CVD-safe)
COLOR_PRIMARY = "#2B5C8F"
COLOR_SECONDARY = "#E66101"

@st.cache_data
def load_data():
    df = pd.read_csv('data/dataset.csv')
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("🔍 Filters")

year_range = st.sidebar.slider(
    "Select Year Range:",
    int(df['Year'].min()),
    int(df['Year'].max()),
    (int(df['Year'].min()), int(df['Year'].max()))
)

regions = st.sidebar.multiselect(
    "Select Regions:",
    options=df['Region'].unique().tolist(),
    default=df['Region'].unique().tolist()
)

status_filter = st.sidebar.radio(
    "Economy Status:",
    options=["All", "Developed", "Developing"]
)

# Filter Dataset
filtered_df = df[
    (df['Year'].between(year_range[0], year_range[1])) &
    (df['Region'].isin(regions))
]

if status_filter == "Developed":
    filtered_df = filtered_df[filtered_df['Economy_status_Developed'] == 1]
elif status_filter == "Developing":
    filtered_df = filtered_df[filtered_df['Economy_status_Developing'] == 1]

# Header
st.title("🌐 Global Health & Development Indicator Dashboard")
st.markdown("Explore key trends in life expectancy, economic indicators, and healthcare metrics across world regions.")

# High-Level Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Life Expectancy", f"{filtered_df['Life_expectancy'].mean():.1f} Years")
col2.metric("Avg GDP per Capita", f"${filtered_df['GDP_per_capita'].mean():,.0f}")
col3.metric("Avg Schooling", f"{filtered_df['Schooling'].mean():.1f} Years")
col4.metric("Avg Infant Deaths", f"{filtered_df['Infant_deaths'].mean():.1f} per 1000")

st.markdown("---")

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📊 Economics & Longevity", "💉 Healthcare & Mortality", "🎓 Education & Nutrition"])

with tab1:
    st.subheader("Economic Impact on Life Expectancy")
    
    # Scatter Plot: GDP vs Life Expectancy
    fig_gdp = px.scatter(
        filtered_df,
        x='GDP_per_capita',
        y='Life_expectancy',
        size='Population_mln',
        color='Region',
        hover_name='Country',
        log_x=True,
        title="Life Expectancy vs. GDP per Capita (Log Scale)",
        template="plotly_white"
    )
    st.plotly_chart(fig_gdp, use_container_width=True)
    
    # Time Series: Life Expectancy over time
    df_trend = filtered_df.groupby(['Year', 'Region'])['Life_expectancy'].mean().reset_index()
    fig_trend = px.line(
        df_trend,
        x='Year',
        y='Life_expectancy',
        color='Region',
        title="Life Expectancy Trends Over Time by Region",
        template="plotly_white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with tab2:
    st.subheader("Healthcare Coverage and Mortality Metrics")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        fig_imm = px.box(
            filtered_df,
            x='Region',
            y='Measles',
            color='Region',
            title="Measles Immunization Coverage (%)",
            template="plotly_white"
        )
        st.plotly_chart(fig_imm, use_container_width=True)
        
    with col_b:
        fig_mort = px.scatter(
            filtered_df,
            x='Incidents_HIV',
            y='Adult_mortality',
            color='Region',
            title="HIV Incidents vs Adult Mortality",
            template="plotly_white"
        )
        st.plotly_chart(fig_mort, use_container_width=True)

with tab3:
    st.subheader("Schooling, BMI, and Nutritional Factors")
    
    fig_edu = px.scatter(
        filtered_df,
        x='Schooling',
        y='Infant_deaths',
        color='Region',
        trendline="ols",
        title="Schooling Years vs. Infant Deaths",
        template="plotly_white"
    )
    st.plotly_chart(fig_edu, use_container_width=True)

    fig_bmi = px.histogram(
        filtered_df,
        x='BMI',
        color='Region',
        barmode='overlay',
        title="BMI Distribution Across Regions",
        template="plotly_white"
    )
    st.plotly_chart(fig_bmi, use_container_width=True)