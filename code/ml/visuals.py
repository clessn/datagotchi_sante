import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from config import Config
from constants import Constants as C
from loaders import load_results_metrics


def welcome():
    # Welcome
    st.write("Welcome on the visuals for Datagotchi Health")


def select_experiment():

    # Select the experiment
    experiments_list = [experiment for experiment in os.listdir(C.EXPERIMENTS_PATH)]
    selected_experiment = st.selectbox(
        "Choose the experiment you want to see", experiments_list
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
    selected_run = st.selectbox(
        "Choose the run of the experiment you want to see", run_unique_df["run"]
    )
    timestamp_selected = run_unique_df[run_unique_df["run"] == selected_run][
        "timestamp"
    ].iloc[0]

    # Find the latest version of the experiment
    # timestamp_selected = metrics_df["timestamp"].max()

    # Keep only the run selected
    metrics_df = metrics_df[metrics_df["timestamp"] == timestamp_selected].copy()

    return metrics_df


def table_metrics_all(metrics_df):

    # Show a table with all results
    st.write("Here is a table with all results")
    metrics_df[["fold_id", "model_name", "metric_name", "metric_value"]]


def plot_results_metric(metrics_df):

    # Select a metric
    metric_choice = st.selectbox(
        "Which metric do you want to plot?", Config.METRIC_LIST
    )

    # Keep only results for this metric
    selected_metric_df = metrics_df[metrics_df["metric_name"] == metric_choice].copy()

    # Group by model
    mean_selected_metric_df = (
        selected_metric_df.groupby("model_name")["metric_value"].mean().reset_index()
    )
    mean_selected_metric_df

    # Create figure
    fig, ax = plt.subplots()
    ax.bar(
        mean_selected_metric_df["model_name"],
        mean_selected_metric_df["metric_value"],
        color="skyblue",
    )
    ax.set_xlabel("Model name")
    ax.set_ylabel(f"Mean value on {metric_choice}")
    ax.set_title(f"Mean value on {metric_choice} for models")

    # Adjust size
    ax.tick_params(axis="x", labelsize=10)
    # Ajust rotation
    plt.xticks(rotation=45, ha="right")
    # Adjust space
    plt.tight_layout()

    # Plot results
    # st.line_chart(mean_selected_metric_df)
    st.pyplot(fig)


welcome()
metrics_df = select_experiment()
table_metrics_all(metrics_df)
plot_results_metric(metrics_df)
