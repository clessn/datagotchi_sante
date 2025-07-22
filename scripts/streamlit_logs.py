from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


# Load the .env file
load_dotenv()

# Log file
LOG_FILENAME = 'Log.csv'


def logs_to_user_status():

    # Load the log file
    track_path = Path(os.getenv("DATA_TRACK_PATH"))
    log_file = track_path / LOG_FILENAME
    log_df = pd.read_csv(log_file, delimiter=",")

    # Convert timestamp to datetime
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

    # For each user, get the last phase they were in and create a dictionary mapping user_id to phase_id
    last_phase = (
        log_df.sort_values('timestamp')
        .groupby('user_id')
        .tail(1)
        .set_index('user_id')['phase_id']
        .to_dict()
    )
    
    return last_phase

# phase order
phase_order = [
    "login", "consent", "sociodemo", "knowledge_before", "lifestyle",
    "explain", "satisfaction", "intent", "knowledge_after", "essaim", "merci"
]

# dict with phase_id for each user_id
last_phase_dict = logs_to_user_status()
phase_series = pd.Series(list(last_phase_dict.values()))
phase_series = pd.Categorical(phase_series, categories=phase_order, ordered=True)

# count per phase
phase_counts = pd.Series(phase_series).value_counts().reindex(phase_order, fill_value=0).astype(int)

# Display the histogram of user phases
st.title("Histogram of users per phase")
st.write("Distribution of last phase_id for users:")
st.bar_chart(phase_counts)

# Dropdown to select a user and display their last phase
st.header("Check last phase for a specific user")
user_ids = sorted(last_phase_dict.keys())
selected_user = st.selectbox("Select a user_id", user_ids)

if selected_user:
    st.write(f"User `{selected_user}` has finished phase: **{last_phase_dict[selected_user]}**")