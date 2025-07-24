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
st.experimental_autorefresh(interval=5000, key="data_refresh")

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
    title="Number of users per phase"
)

st.plotly_chart(fig, use_container_width=True)

# ---- USER SELECTION ----
st.header("Check last phase for a specific user")

user_ids = sorted(last_phase_dict.keys())

# Preserve user selection across refreshes
if "selected_user" not in st.session_state:
    st.session_state.selected_user = user_ids[0] if user_ids else None

selected_index = 0
if st.session_state.selected_user in user_ids:
    selected_index = user_ids.index(st.session_state.selected_user)

selected_user = st.selectbox(
    "Select a user_id",
    user_ids,
    index=selected_index,
    key="selected_user"
)

if selected_user:
    st.write(f"User `{selected_user}` has finished phase: **{last_phase_dict[selected_user]}**")

    user_logs = log_df[log_df['user_id'] == selected_user]

    st.subheader("All logs for selected user")
    st.dataframe(user_logs)
