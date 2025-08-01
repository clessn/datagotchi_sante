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
# User file
USER_FILENAME = 'User.csv'

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

def download_users():

    # Load the user file
    track_path = Path(os.getenv("DATA_TRACK_PATH"))
    user_file = track_path / USER_FILENAME
    user_df = pd.read_csv(user_file, delimiter=",")

    return user_df
    
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
        batch_info_dict[csv_file.stem] = df

    return batch_info_dict

def select_batch(log_df, batch_info_dict):

    # batch names
    batch_keys = sorted(batch_info_dict.keys(), reverse=True)
    if "pretest" in batch_keys:
        # I want pretest to be the last option
        batch_keys.remove("pretest")
        batch_keys.append("pretest")
    # select a batch to use
    batch_options = ["new batch"] + batch_keys
    batch_name = st.selectbox("Select a batch", batch_options)

    if batch_name == "new batch":
        # select all users from all batches
        all_batch_users = set()
        for df in batch_info_dict.values():
            all_batch_users.update(df['Participant id'].unique())
        # select users not in any batch and not used for the test
        users_selected = [
            uid for uid in log_df['user_id'].unique()
            if uid not in all_batch_users and "test" not in str(uid).lower()
        ]
    else:
        # select all users from the chosen batch
        users_selected = batch_info_dict[batch_name]['Participant id'].tolist()

    return users_selected, batch_name

# Verify if a user passed the attention checks
def attention_check_user(logs, user_id):
    # Verify the attention check for knowledge_before
    before = logs[
        (logs['user_id'] == user_id) &
        (logs['answer_id'] == 'knowledge_04_01') &
        (logs['phase_id'] == 'knowledge_before')
    ]
    # Verify the attention check for knowledge_after
    after = logs[
        (logs['user_id'] == user_id) &
        (logs['answer_id'] == 'knowledge_04_01') &
        (logs['phase_id'] == 'knowledge_after')
    ]
    # Both should exist
    return not before.empty and not after.empty

def get_users_approval(logs, batch_df):
    """
    Displays the approval status of users in a batch.
    
    Args:
        logs (pd.DataFrame): DataFrame containing logs.
        batch_df (pd.DataFrame): DataFrame containing batch information.
    """
    to_approve = []
    to_reject = []
    to_check = []
    approved = []
    refused_timed_out = []
    refused_returned = []
    refused_rejected = []

    # Iterate over each user in the batch
    for _, user in batch_df.iterrows():
        user_id = user['Participant id']
        user_status = user['Status']
        if user_status =='APPROVED':
            approved.append(user_id)
        elif user_status == 'TIME-OUT':
            refused_timed_out.append(user_id)
        elif user_status == 'RETURNED':
            refused_returned.append(user_id)
        elif user_status == 'REJECTED':
            refused_rejected.append(user_id)
        elif user_status == 'AWAITING REVIEW':
            attention_check = attention_check_user(logs, user_id)
            if attention_check:
                if user['Completion code'] == os.getenv("PROLIFIC_COMPLETION_CODE"):
                    to_approve.append(user_id)
                else:
                    # check manually users failing completion code but succeeding attention checks
                    to_check.append(user_id)
            else:
                to_reject.append(user_id)

    return to_approve, to_reject, to_check, approved, refused_timed_out, refused_returned, refused_rejected

def show_users_approval(to_approve, to_reject, to_check, approved, refused_timed_out, refused_returned, refused_rejected):
    
    # Users to approve
    if to_approve:
        st.subheader("Users to approve")
        st.write(", ".join(str(u) for u in to_approve))

    # Users to reject
    if to_reject:
        st.subheader("Users to reject")
        st.write("Users to reject because they failed attention checks")
        st.write(", ".join(str(u) for u in to_reject))

    # Users to check manually
    if to_check:
        st.subheader("Users to check manually")
        st.write("Users to check manually because they passed attention checks but failed completion code")
        st.write(", ".join(str(u) for u in to_check))

    # Approved users
    if approved:
        st.subheader("Approved users")
        st.write(", ".join(str(u) for u in approved))

    # Refused users
    if refused_timed_out or refused_returned or refused_rejected:
        st.subheader("Refused users")
        if refused_timed_out:
            st.markdown(f"**Timed-out** :  \n{', '.join(str(u) for u in refused_timed_out)}")
        if refused_returned:
            st.markdown(f"**Returned** :  \n{', '.join(str(u) for u in refused_returned)}")
        if refused_rejected:
            st.markdown(f"**Rejected** :  \n{', '.join(str(u) for u in refused_rejected)}")

def users_per_explanation(user_df, approved_user_ids):
    st.header("Users per explanation type (approved users only)")

    # Filtrer uniquement les utilisateurs approuvés
    filtered_df = user_df[user_df['user_id'].isin(approved_user_ids)]

    # Compter le nombre d'utilisateurs par condition_id
    condition_counts = filtered_df['condition_id'].value_counts().sort_index()

    # Préparer le DataFrame pour le plot
    df_plot = pd.DataFrame({
        "Condition": condition_counts.index,
        "Users": condition_counts.values
    })

    # Afficher l'histogramme
    fig = px.bar(df_plot, x="Condition", y="Users",
                 labels={"Condition": "Condition ID", "Users": "Number of users"},
                 title="Number of users per explanation type (approved only)")
    st.plotly_chart(fig)

# identify approved users from all batches
def approved_users(batch_info_dict):
    approved_users_set = set()
    for batch_df in batch_info_dict.values():
        approved_users_set.update(batch_df[batch_df['Status'] == 'APPROVED']['Participant id'].unique())
    return list(approved_users_set)

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

# all logs from track folder
log_df = download_logs()

# all users from track folder
user_df = download_users()

# read batch of experiment
batch_info_dict = get_batch_info()

# select a batch of users and batch_name
users_selected, batch_name = select_batch(log_df, batch_info_dict)

# logs for a batch of users
log_df_bacth = logs_for_specific_users(log_df, users_selected)

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

# Approbation of a batch of users
if batch_name!= "new batch":
    st.header("Users' approbation")
    batch_df = batch_info_dict[batch_name]
    to_approve, to_reject, to_check, approved, refused_timed_out, refused_returned, refused_rejected = get_users_approval(logs, batch_df)
    show_users_approval(to_approve, to_reject, to_check, approved, refused_timed_out, refused_returned, refused_rejected)

# global users approved (list of their ids)
approved_users_global = approved_users(batch_info_dict)

# users per explanation type
users_per_explanation(user_df, approved_users_global)