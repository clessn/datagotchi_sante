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

# User batch info folder
USER_BATCH_INFO_FOLDER = 'user_batch_info'

############################
######## Functions #########
############################

def download_logs():

    # Load the log file
    track_path = Path(os.getenv("DATA_TRACK_PATH"))
    log_file = track_path / LOG_FILENAME
    log_df = pd.read_csv(log_file, delimiter=",")

    # Convert timestamp to datetime
    log_df['timestamp'] = pd.to_datetime(log_df['timestamp'])

    return log_df
    
def get_last_phase(log_df):

    # For each user, get the last phase they were in and create a dictionary mapping user_id to phase_id
    last_phase = (
        log_df.sort_values('timestamp')
        .groupby('user_id')
        .tail(1)
        .set_index('user_id')['phase_id']
        .to_dict()
    )
    
    return last_phase

# Keep only the logs for specific users
def logs_for_specific_users(log_df, user_ids):
    """
    Filters the log DataFrame to include only the specified user IDs.
    
    Args:
        log_df (pd.DataFrame): The DataFrame containing logs.
        user_ids (list): List of user IDs to filter by.
        
    Returns:
        pd.DataFrame: Filtered DataFrame with only specified user IDs.
    """
    log_df_filtered = log_df[log_df['user_id'].isin(user_ids)]
    return log_df_filtered

def get_batch_info():
    result_path = Path(os.getenv("DATA_RESULT_PATH"))
    user_batch_info_path = result_path / USER_BATCH_INFO_FOLDER

    batch_info_dict = {}
    for csv_file in user_batch_info_path.glob("*.csv"):
        df = pd.read_csv(csv_file)
        batch_info_dict[csv_file.name] = df

    return batch_info_dict

############################
######## Streamlit #########
############################

# Page title
st.title("Histogram of users per phase")

# phase order
phase_order = [
    "login", "consent", "sociodemo", "knowledge_before", "lifestyle",
    "explain", "satisfaction", "intent", "knowledge_after", "essaim", "merci"
]

# read batch of experiment
batch_info_dict = get_batch_info()

# select a batch to use
batch_name = st.selectbox("Select a batch", list(batch_info_dict.keys()))
users_from_batch = batch_info_dict[batch_name]['Participant id'].tolist()

# all logs from track folder
log_df = download_logs()

# logs for a batch of users
log_df_bacth = logs_for_specific_users(log_df, users_from_batch)

# select logs to use
logs = log_df_bacth # logs for a specific batch of users
# logs = log_df # all logs

# dict with phase_id for each user_id
last_phase_dict = get_last_phase(logs)

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
    user_logs = logs[logs['user_id'] == selected_user]

    st.subheader("All logs for selected user")
    st.dataframe(user_logs)
