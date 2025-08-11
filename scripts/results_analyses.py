from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd

# Load the .env file
load_dotenv()

##########################
####### Constants ########
##########################
USER_BATCH_INFO_FOLDER = "user_batch_info"


##########################
####### Functions ########
##########################

# Read info from Prolific 
def get_batch_info():
    result_path = Path(os.getenv("DATA_RESULT_PATH"))
    user_batch_info_path = result_path / USER_BATCH_INFO_FOLDER

    batch_info_dict = {}
    for csv_file in user_batch_info_path.glob("*.csv"):
        df = pd.read_csv(csv_file)
        batch_info_dict[csv_file.stem] = df

    return batch_info_dict

# Get a list of ids of users approved on Prolific
def approved_users(batch_info_dict):
    approved_users_set = set()
    for batch_df in batch_info_dict.values():
        approved_users_set.update(batch_df[batch_df['Status'] == 'APPROVED']['Participant id'].unique())
    return list(approved_users_set)


def read_prolific_and_logs():

    # read batch of experiment
    prolific_info_dict = get_batch_info()
    #print(prolific_info_dict)

    # list of ids of users approved on Prolific
    approved_users_list = approved_users(prolific_info_dict)
    print(approved_users_list)
    print("Tous les éléments sont uniques :", len(approved_users_list) == len(set(approved_users_list)))



