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

# Batch selected folder
BATCH_SELECTED = 'batch_06'

# clean folder
CLEAN_FOLDER = 'clean'

# Correspondence between question ids and manipulation check
MANIPULATION_DICO ={
    "satis_09": "manipulation_visual",
    "satis_10": "manipulation_textual",
    "satis_11": "manipulation_numerical",
    "satis_12": "manipulation_interactive",
    "satis_13": "manipulation_contextual"
}

# correspondence between question ids and intent names
INTENT_DICO = {
    "intent_01": "intention_sleep",
    "intent_02": "importance_sleep",
    "intent_03": "intention_diet",
    "intent_04": "importance_diet",
    "intent_05": "intention_social",
    "intent_06": "importance_social",
    "intent_07": "intention_neighborhood",
    "intent_08": "importance_neighborhood",
    "intent_09": "intention_volunteering",
    "intent_10": "importance_volunteering"
}

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
####### Filter DB ########
##########################

# Get a list of ids of users approved on Prolific
def approved_users(batch_info_dict):
    approved_users_set = set()
    for batch_df in batch_info_dict.values():
        approved_users_set.update(batch_df[batch_df['Status'] == 'APPROVED']['Participant id'].unique())
    return list(approved_users_set)

# Get a list of ids of users who passed the attention check
def attention_check_users(logs, users):

    attention_check_users_list = []

    for user_id in users:

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

        # If the user passed the attention check in both phases, add to the list
        if not before.empty and not after.empty:
            attention_check_users_list.append(user_id)

    return attention_check_users_list

# Filter logs and users based on a list of user ids
def filter_logs_users(user_ids_list, logs_raw, users_raw):
    logs_filtered = logs_raw[logs_raw['user_id'].isin(user_ids_list)]
    users_filtered = users_raw[users_raw['user_id'].isin(user_ids_list)]
    return logs_filtered, users_filtered

# Filter DB and write results to csv files
def write_filtered_db():

    # read batch of experiment
    prolific_info_dict = get_batch_info()

    # read db of results
    logs_raw, users_raw, questions_raw, answers_raw = read_results()

    # list of ids of users approved on Prolific
    prolific_approved_users_list = approved_users(prolific_info_dict)

    # list of ids of approved users who passed the attention check
    experiment_approved_users_list = attention_check_users(logs_raw, prolific_approved_users_list)

    # keep results only for approved users
    logs, users = filter_logs_users(experiment_approved_users_list, logs_raw, users_raw)

    # write filtered results to csv files
    clean_path = Path(os.getenv("DATA_RESULT_PATH")) / CLEAN_FOLDER
    logs.to_csv(clean_path / LOG_FILENAME, index=False)
    users.to_csv(clean_path / USER_FILENAME, index=False)
    questions_raw.to_csv(clean_path / QUESTION_FILENAME, index=False)
    answers_raw.to_csv(clean_path / ANSWER_FILENAME, index=False)

##########################
#### Compute scores ######
##########################

# Read cleaned db
def read_cleaned_db():
    clean_path = Path(os.getenv("DATA_RESULT_PATH")) / CLEAN_FOLDER
    logs = pd.read_csv(clean_path / LOG_FILENAME)
    users = pd.read_csv(clean_path / USER_FILENAME)
    questions = pd.read_csv(clean_path / QUESTION_FILENAME)
    answers = pd.read_csv(clean_path / ANSWER_FILENAME)
    return logs, users, questions, answers


# Get logs for a phase
def get_phase_logs(logs, phase_id, questions_ids):

    # Keep logs for the specified phase_id and question_ids
    filtered_logs = logs[
        (logs['phase_id'] == phase_id) &
        (logs['question_id'].isin(questions_ids))
    ]
    # For each question_id, keep only the log with the most recent timestamp
    latest_logs_df = filtered_logs.loc[filtered_logs.groupby('question_id')['timestamp'].idxmax()]
    
    return latest_logs_df

# Compute knowledge score based on logs
def get_average_score(logs, answers):
    sum_answer_values = 0
    for log in logs.itertuples():
        # Get the answer_id and its corresponding value
        answer_id = log.answer_id
        answer_value = answers[answers['answer_id'] == answer_id]['answer_weight'].iloc[0]
        sum_answer_values += answer_value

    return sum_answer_values/len(logs)

# Compute essaim score based on logs
def get_essaim_score(logs, answers):
    sum_answer_values = 0
    for log in logs.itertuples():
        # Get the answer_id and its corresponding value
        answer_id = log.answer_id
        answer_value = answers[answers['answer_id'] == answer_id]['answer_weight'].iloc[0]
        sum_answer_values += answer_value-1 #we remove 1 because it is based on a 1-6 scale, we want a 0-5 scale
    # we want a 0-100 scale, instead of 0-70 scale
    return (sum_answer_values/70) * 100

def get_manipulation_values(logs, answers):
    # create a dictionary to hold manipulation values
    manipulation_values = {qid: None for qid in MANIPULATION_DICO.keys()}
    for log in logs.itertuples():
        # Get the answer_id and its corresponding value
        answer_id = log.answer_id
        answer_value = answers[answers['answer_id'] == answer_id]['answer_weight'].iloc[0]
        manipulation_values[log.question_id] = answer_value
        
    return manipulation_values

#def get_intent_values(logs, answers):
    #for log in logs.itertuples():
        # Get the answer_id and its corresponding value
        #answer_id = log.answer_id
        #answer_value = answers[answers['answer_id'] == answer_id]['answer_weight'].iloc[0]
        
        

def clean_results():

    # read results from the database filtered
    logs, users, questions, answers = read_cleaned_db()
    # convert timestamp from string to datetime
    logs['timestamp'] = pd.to_datetime(logs['timestamp'])

    # create df with unique user ids
    unique_users = users['user_id'].unique()
    results_df = pd.DataFrame(unique_users, columns=['user_id'])

    for user_id in unique_users:
        
        # logs of the user
        user_logs = logs[logs['user_id'] == user_id]

        ############
        # study duration
        ############

        start_time = user_logs.loc[user_logs['log_type'] == 'started', 'timestamp'].min()
        end_time = user_logs.loc[user_logs['log_type'] == 'finished', 'timestamp'].max()
        study_duration = end_time - start_time
        results_df.loc[results_df['user_id'] == user_id, 'study_duration'] = study_duration

        ############
        # knowledge before and after scores
        ############

        # get questions ids for knowledge phase, excluding knowledge_04 which is the attention check
        knowledge_questions_ids = questions[(questions['group_id'] == 'knowledge') & (questions['question_id'] != 'knowledge_04')]['question_id'].tolist()
        # get logs for knowledge before and after phases
        knowledge_before_logs = get_phase_logs(user_logs, 'knowledge_before', knowledge_questions_ids)
        knowledge_after_logs = get_phase_logs(user_logs, 'knowledge_after', knowledge_questions_ids)
        # compute scores
        knowledge_before_score = get_average_score(knowledge_before_logs, answers)
        knowledge_after_score = get_average_score(knowledge_after_logs, answers)
        # save scores
        results_df.loc[results_df['user_id'] == user_id, 'knowledge_before_score'] = knowledge_before_score
        results_df.loc[results_df['user_id'] == user_id, 'knowledge_after_score'] = knowledge_after_score
        
        ############
        # explain phase
        ############

        # explain type
        explain_type = users[users['user_id'] == user_id]['condition_id'].values[0]
        results_df.loc[results_df['user_id'] == user_id, 'explain_type'] = explain_type
        
        # explain logs
        explain_logs = user_logs[user_logs['phase_id'] == 'explain']

        # count iteration of retry for interactive explain, None for others because not applicable
        if explain_type == 'explain_interactive':
            results_df.loc[results_df['user_id'] == user_id, 'explain_retry'] = len(explain_logs)
        else:
            results_df.loc[results_df['user_id'] == user_id, 'explain_retry'] = None
        
        # first explain log timestamp, corresonding to the score computed by the algorithm
        min_timestamp_idx = explain_logs['timestamp'].idxmin()
        # predicted well-being score by the algorithm after lifestyle questions
        predicted_wellbeing_score = explain_logs.loc[min_timestamp_idx, 'log_info']
        results_df.loc[results_df['user_id'] == user_id, 'predicted_wellbeing_score'] = predicted_wellbeing_score
        
        ############
        # essaim score
        ############
        # get questions ids for essaim phase
        essaim_questions_ids = questions[(questions['group_id'] == 'essaim')]['question_id'].tolist()
        # get logs for knowledge before and after phases
        essaim_logs = get_phase_logs(user_logs, 'essaim', essaim_questions_ids)
        # compute scores
        essaim_score = get_essaim_score(essaim_logs, answers)
        # save scores
        results_df.loc[results_df['user_id'] == user_id, 'observed_wellbeing_score'] = essaim_score
        
        ############
        # manipulation variables
        ############
        # get questions ids for manipulation questions in the satisfaction phase
        manipulation_question_ids = list(MANIPULATION_DICO.keys())
        # get logs for manipulation questions
        manipulation_logs = get_phase_logs(user_logs, 'satisfaction', manipulation_question_ids)
        # get manipulation values
        manipulation_values = get_manipulation_values(manipulation_logs, answers)
        # save manipulation variables
        for raw_name, value in manipulation_values.items():
            clean_name = MANIPULATION_DICO[raw_name]
            results_df.loc[results_df['user_id'] == user_id, clean_name] = value
        
        ############
        # satisfaction score
        ############
        # get questions ids for satisfaction phase
        satisfaction_questions_ids = questions[(questions['group_id'] == 'satisfaction') & (~questions['question_id'].isin(manipulation_question_ids))]['question_id'].tolist()
        # get logs for mediation questions
        satisfaction_logs = get_phase_logs(user_logs, 'satisfaction', satisfaction_questions_ids)
        # compute score
        satisfaction_score = get_average_score(satisfaction_logs, answers)
        # save scores
        results_df.loc[results_df['user_id'] == user_id, 'satisfaction_score'] = satisfaction_score
        
        
    print(results_df.head())