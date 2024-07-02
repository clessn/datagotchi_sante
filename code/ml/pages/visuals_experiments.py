import os
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from configs.visuals import VisualsConfig as Config
from constants import Constants as C
from loaders import load_config, load_results_metrics
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

    # Load metrics results
    metrics_df = load_results_metrics(experiments_path / selected_experiment, C.METRICS_FILENAME)
    # Convert timestamp into datetime
    metrics_df["timestamp"] = pd.to_datetime(metrics_df["timestamp"])

    # Find unique run
    run_unique_df = metrics_df.drop_duplicates(subset=["run_id", "timestamp"])[
        ["run_id", "timestamp"]
    ]
    # Order by timestamp
    run_unique_df = run_unique_df.sort_values(by="timestamp", ascending=False)
    # Combine run_id and timestamp
    run_unique_df["run"] = (
        run_unique_df["run_id"] + " - " + run_unique_df["timestamp"].astype(str)
    )

    # Select the run
    selected_run = st.sidebar.selectbox(
        "Choose the run of the experiment you want to see", run_unique_df["run"]
    )
    selected_timestamp = run_unique_df[run_unique_df["run"] == selected_run][
        "timestamp"
    ].iloc[0]
    selected_run_name = run_unique_df[run_unique_df["run"] == selected_run][
        "run_id"
    ].iloc[0]

    # Keep only the run selected
    metrics_df = metrics_df[metrics_df["timestamp"] == selected_timestamp].copy()

    return metrics_df, selected_experiment, selected_run_name


### Show a table with results of a run
def table_metrics_all(metrics_df):

    # Show a table with all results
    st.write("Here is a table with all results")
    metrics_df[["fold_id", "model_name", "metric_name", "metric_value"]]


### Plot results of a run
def plot_results_metric(metrics_df):

    # List with available metrics for this run
    metric_list = np.unique(metrics_df["metric_name"])
    
    # Select the metric
    metric_choice = st.sidebar.selectbox(
        "Which metric do you want to plot?", metric_list
    )

    # Keep only results for this metric
    selected_metric_df = metrics_df[metrics_df["metric_name"] == metric_choice].copy()

    # Group by model
    mean_selected_metric_df = (
        selected_metric_df.groupby("model_name")["metric_value"].mean().reset_index()
    )

    # Create plot using plotly
    fig = px.bar(
        mean_selected_metric_df,
        x="model_name",
        y="metric_value",
        title=f"Mean value on {metric_choice} for models",
        labels={
            "model_name": "Model name",
            "metric_value": f"Mean value on {metric_choice}",
        },
    )

    # Rotate x-axis labels
    fig.update_layout(xaxis_tickangle=-45)

    # Plot results
    st.plotly_chart(fig)


### Show configuration of this run
def show_config(experiments_path, selected_experiment, selected_run_name):
    st.write("Configuration for this run of experiment")
    selected_run_path = (
        experiments_path
        / selected_experiment
        / C.EXPERIMENTS_ARTIFACTS_FOLDER_NAME
        / selected_run_name
    )
    config_df = load_config(selected_run_path)
    config_df


###################### Preloading  ########################

# Derive paths from configs
ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
experiments_path = ml_run_path / C.EXPERIMENTS_FOLDER_NAME


##################### Content page ########################

# Sidebarmenu
menu()

# Text
st.title("Experiments")

# Selection of the run and loading results of it
metrics_df, selected_experiment, selected_run_name = select_experiment(experiments_path)

# Select a metric and visualize results of the run
# table_metrics_all(metrics_df)
plot_results_metric(metrics_df)

# Show config for this run
show_config(experiments_path, selected_experiment, selected_run_name)
