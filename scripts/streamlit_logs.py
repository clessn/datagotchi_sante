from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import streamlit as st
import plotly.express as px

# Load the .env file
load_dotenv()

LOG_FILENAME = 'Log.csv'

def logs_to_user_status():
    track_path = Path(os.getenv("DATA_TRACK_PATH"))
    log_file = track_path / LOG_FILENAME
    log_df = pd.read_csv(log_file, delimiter=",")
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

    last_phase = (
        log_df.sort_values('timestamp')
        .groupby('user_id')
        .tail(1)
        .set_index('user_id')['phase_id']
        .to_dict()
    )
    return last_phase, log_df

# ---- AUTO REFRESH EVERY 5 SECONDS ----
st_autorefresh = st.experimental_rerun  # alias for clarity
st_autorefresh = st.experimental_rerun  # alias for clarity

st_autorefresh = st.autorefresh(interval=5_000, key="data_refresh")

# ---- PAGE TITLE ----
st.title("Histogram of users per phase")

phase_order = [
    "login", "consent", "sociodemo", "knowledge_before", "lifestyle",
    "explain", "satisfaction", "intent", "knowledge_after", "essaim", "merci"
]

last_phase_dict, log_df = logs_to_user_status()

# ---- HISTOGRAM ----
phase_counts = pd.Series(last_phase_dict).value_counts().reindex(phase_order, fill_value=0).astype(int)

df_plot = pd.DataFrame({
    "Phase": phase_order,
    "Users": phase_counts.values
})

fig = px.bar(
    df_plot, x="Phase", y="Users",
    labels={"Phase": "Phase", "Users": "Number of users"},
    title="Number of u
