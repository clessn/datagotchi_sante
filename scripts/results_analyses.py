from dotenv import load_dotenv
from pathlib import Path
import os
import pandas as pd

# Load the .env file
load_dotenv()

##########################
####### Constants ########
##########################

# info folder from prolific
USER_BATCH_INFO_FOLDER = "user_batch_info"

# Log file
LOG_FILENAME = 'Log.csv'
# User file
USER_FILENAME = 'User.csv'
# Question file
QUESTION_FILENAME = 'Question.csv'  
# Answer file
ANSWER_FILENAME = 'Answer.csv'

# Batch selected
BATCH_SELECTED = 'batch_06'


##########################
#### Reading functions ###
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

# Read results from the database
def read_results():
    result_path = Path(os.getenv("DATA_RESULT_PATH"))
    batch_result_path = result_path / BATCH_SELECTED 
    logs = pd.read_csv(batch_result_path / LOG_FILENAME)
    users = pd.read_csv(batch_result_path / USER_FILENAME)
    questions = pd.read_csv(batch_result_path / QUESTION_FILENAME)
    answers = pd.read_csv(batch_result_path / ANSWER_FILENAME)
    return logs, users, questions, answers

##########################
#### Other functions #####
##########################

# Get a list of ids of users approved on Prolific
def approved_users(batch_info_dict):
    approved_users_set = set()
    for batch_df in batch_info_dict.values():
        approved_users_set.update(batch_df[batch_df['Status'] == 'APPROVED']['Participant id'].unique())
    return list(approved_users_set)


##########################
######### Main ###########
##########################

def read_prolific_and_logs():

    # read batch of experiment
    prolific_info_dict = get_batch_info()

    # read db of results
    logs, users, questions, answers = read_results()

    # list of ids of users approved on Prolific
    approved_users_list = approved_users(prolific_info_dict)



