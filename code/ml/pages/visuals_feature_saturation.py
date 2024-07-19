import os

import plotly.express as px
import streamlit as st
from configs.visuals import VisualsConfig as Config
from constants import Constants as C
from visuals import menu

###################### Functions  ########################

### Select an experiment
def select_experiment(experiments_path):

    # Title of sidebar
    st.sidebar.title("Selection of the experiment")

    # Select the experiment
    experiments_list = [experiment for experiment in os.listdir(experiments_path)]
    experiments_list_sorted = sorted(experiments_list, reverse=True)
    selected_experiment = st.sidebar.selectbox(
        "Choose the experiment you want to see", experiments_list_sorted
    )
    return selected_experiment


###################### Preloading  ########################

# Derive paths from configs
ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
experiments_path = ml_run_path / C.EXPERIMENTS_FOLDER_NAME

###################### Content page ##########################

# Sidebarmenu
menu()

# Text
st.title("Feature Selection Saturation")

# Experiment selection
select_experiment(experiments_path)