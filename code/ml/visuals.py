import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from config import Config
from constants import Constants as C
from loaders import load_results_metrics, load_config


def welcome():
    # Welcome
    st.title("Visuals for Datagotchi Health")


def select_experiment():

    # Select the experiment
    experiments_list = [experiment for experiment in os.listdir(C.EXPERIMENTS_PATH)]
    experiments_list_sorted = sorted(experiments_list, reverse=True)
    selected_experiment = st.sidebar.selectbox(
        "Choose the experiment you want to see", experiments_list_sorted
    )

    # Load metrics results
    metrics_df = load_results_metrics(experiment_name=selected_experiment)
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
    timestamp_selected = run_unique_df[run_unique_df["run"] == selected_run][
        "timestamp"
    ].iloc[0]
    selected_run_name = run_unique_df[run_unique_df["run"] == selected_run][
        "run_id"
    ].iloc[0]

    # Keep only the run selected
    metrics_df = metrics_df[metrics_df["timestamp"] == timestamp_selected].copy()

    return metrics_df, selected_experiment, selected_run_name


def table_metrics_all(metrics_df):

    # Show a table with all results
    st.write("Here is a table with all results")
    metrics_df[["fold_id", "model_name", "metric_name", "metric_value"]]


def plot_results_metric(metrics_df):

    # Select a metric
    metric_choice = st.sidebar.selectbox(
        "Which metric do you want to plot?", Config.METRIC_LIST
    )

    # Keep only results for this metric
    selected_metric_df = metrics_df[metrics_df["metric_name"] == metric_choice].copy()

    # Group by model
    mean_selected_metric_df = (
        selected_metric_df.groupby("model_name")["metric_value"].mean().reset_index()
    )

    # Create figure
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(
        mean_selected_metric_df["model_name"],
        mean_selected_metric_df["metric_value"],
        color="skyblue",
    )
    ax.set_xlabel("Model name", fontsize=12)
    ax.set_ylabel(f"Mean value on {metric_choice}", fontsize=12)
    ax.set_title(f"Mean value on {metric_choice} for models", fontsize=16)

    for bar, metric_value in zip(bars, mean_selected_metric_df["metric_value"]):
        ax.text(bar.get_x() + bar.get_width() / 2.0, metric_value, f'{metric_value:.2f}', va='bottom', ha='center')

    # Adjust size
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)
    # Ajust rotation
    plt.xticks(rotation=45, ha="right")
    # Adjust space
    plt.tight_layout()

    # Plot results
    st.pyplot(fig)

def show_config(selected_experiment, selected_run_name):
    st.write("Configuration for this run of experiment")
    selected_run_path = C.EXPERIMENTS_PATH / selected_experiment / C.EXPERIMENTS_ARTIFACTS_FOLDER_NAME / selected_run_name
    config_df = load_config(selected_run_path)
    config_df
    


welcome()
metrics_df, selected_experiment, selected_run_name = select_experiment()
#table_metrics_all(metrics_df)
plot_results_metric(metrics_df)
show_config(selected_experiment, selected_run_name)
