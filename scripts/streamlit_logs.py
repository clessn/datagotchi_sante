from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd
import streamlit as st
import plotly.express as px


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

# Page title
st.title("Histogram of users per phase")

# phase order
phase_order = [
    "login", "consent", "sociodemo", "knowledge_before", "lifestyle",
    "explain", "satisfaction", "intent", "knowledge_after", "essaim", "merci"
]

# dict with phase_id for each user_id
last_phase_dict = logs_to_user_status()

# count per phase
phase_counts = pd.Series(last_phase_dict).value_counts().reindex(phase_order, fill_value=0).astype(int)

# Display the histogram of user phases
df_plot = pd.DataFrame({
    "Phase": phase_order,
    "Users": phase_counts.values
})

fig = px.bar(df_plot, x="Phase", y="Users",
             labels={"Phase": "Phase", "Users": "Number of users"},
             title="Number of users per phase")

st.plotly_chart(fig)

# Dropdown to select a user and display their last phase
st.header("Check last phase for a specific user")
user_ids = sorted(last_phase_dict.keys())
selected_user = st.selectbox("Select a user_id", user_ids)

if selected_user:
    st.write(f"User `{selected_user}` has finished phase: **{last_phase_dict[selected_user]}**")
    
    # Display all logs for this user
    track_path = Path(os.getenv("DATA_TRACK_PATH"))
    log_file = track_path / LOG_FILENAME
    log_df = pd.read_csv(log_file, delimiter=",")
    user_logs = log_df[log_df['user_id'] == selected_user]

    st.subheader("All logs for selected user")
    st.dataframe(user_logs)