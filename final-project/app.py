import os
import pathlib
import pandas as pd
import streamlit as st

# Gets the directory where app.py lives (.../final-project)
APP_DIR = pathlib.Path(__file__).parent.resolve()
# Gets the root repository directory (.../dataviz-exercises-suniltejh361)
REPO_ROOT = APP_DIR.parent.resolve()

@st.cache_data
def load_data():
    # 1. Try Root data folder (e.g. repo_root/data/...)
    root_data = REPO_ROOT / "data" / "dataset.csv"
    root_data_alt = REPO_ROOT / "data" / "data set viz.csv"
    
    # 2. Try Local app data folder (e.g. final-project/data/...)
    local_data = APP_DIR / "data" / "dataset.csv"
    local_data_alt = APP_DIR / "data" / "data set viz.csv"

    if root_data.exists():
        return pd.read_csv(root_data)
    elif root_data_alt.exists():
        return pd.read_csv(root_data_alt)
    elif local_data.exists():
        return pd.read_csv(local_data)
    elif local_data_alt.exists():
        return pd.read_csv(local_data_alt)
    else:
        # Fallback to standard relative read
        return pd.read_csv("../data/dataset.csv")
