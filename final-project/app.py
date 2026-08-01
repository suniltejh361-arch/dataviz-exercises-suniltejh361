from pathlib import Path
import os
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Data Visualization Dashboard",
    page_icon="📊",
    layout="wide",
)

# 2. ROBUST DATA LOADING LOGIC
# Determine absolute directory paths to handle Streamlit Cloud execution
CURRENT_DIR = Path(__file__).resolve().parent  # final-project/
REPO_ROOT = CURRENT_DIR.parent  # repo root/

# List of probable names for your CSV file (Update if your filename is different!)
POSSIBLE_FILENAMES = ["dataset.csv", "data.csv", "Final_Project.csv", "cleaned_data.csv"]

# Build candidate paths across both local and cloud folder structures
candidate_paths = []
for fname in POSSIBLE_FILENAMES:
    candidate_paths.extend(
        [
            CURRENT_DIR / "data" / fname,
            CURRENT_DIR / fname,
            REPO_ROOT / "data" / fname,
            REPO_ROOT / fname,
        ]
    )

# Search for the dataset
data_path = None
for path in candidate_paths:
    if path.exists() and path.is_file():
        data_path = path
        break


@st.cache_data
def load_data(file_path):
    return pd.read_csv(file_path)


# Check if dataset was located
if data_path is None:
    st.error("🚨 Dataset File Not Found!")
    st.write(
        "Streamlit couldn't locate your CSV file. Checked the following paths:"
    )
    for p in candidate_paths[:4]:
        st.code(str(p))
    st.info(
        "💡 **Fix:** Make sure your CSV file is uploaded inside the `data/` or `final-project/` folder in your GitHub repository."
    )
    st.stop()

# Load the dataset
try:
    df = load_data(data_path)
except Exception as e:
    st.error(f"Error reading dataset: {e}")
    st.stop()

# 3. DASHBOARD UI LOGIC
st.title("📊 Data Visualization Dashboard")
st.markdown("---")

# Quick KPI Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Total Records", value=f"{len(df):,}")
with col2:
    st.metric(label="Total Columns", value=len(df.columns))
with col3:
    st.metric(label="Dataset Source", value=data_path.name)

st.markdown("---")

# Dataset Preview
st.subheader("📋 Dataset Preview")
st.dataframe(df.head(100), use_container_width=True)

# Interactive Chart Section
st.markdown("---")
st.subheader("📈 Interactive Explorer")

numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()
categorical_cols = df.select_dtypes(
    include=["object", "category"]
).columns.tolist()

if numeric_cols:
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        x_axis = st.selectbox("Select X-Axis", options=df.columns, index=0)
    with chart_col2:
        y_axis = st.selectbox(
            "Select Y-Axis",
            options=numeric_cols,
            index=0 if len(numeric_cols) > 0 else 0,
        )

    fig = px.histogram(
        df,
        x=x_axis,
        y=y_axis,
        title=f"{y_axis} by {x_axis}",
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No numeric columns found for plotting.")
