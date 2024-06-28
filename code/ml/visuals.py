import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from config import Config
from constants import Constants as C
from feature_selection import available_feature_selection
from loaders import load_results_metrics, load_config, load_scores_features


def welcome():
    # Welcome
    st.title("Visuals for Datagotchi Health")


def select_experiment():

    # Title of sidebar
    st.sidebar.title("Selection of the experiment")

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

    # Title plot
    st.write(f"Mean value on {metric_choice} for models")

    # Plot results
    st.bar_chart(
        mean_selected_metric_df.set_index("model_name"),
        #x = "model_name",
        #y = f"Mean value on {metric_choice}"
        )
    

def show_config(selected_experiment, selected_run_name):
    st.write("Configuration for this run of experiment")
    selected_run_path = C.EXPERIMENTS_PATH / selected_experiment / C.EXPERIMENTS_ARTIFACTS_FOLDER_NAME / selected_run_name
    config_df = load_config(selected_run_path)
    config_df

def select_feature_selection_method():

    # Title of sidebar
    st.sidebar.title("Feature selection")

    # Selection of the feature selection method
    selected_feature_selection_method = st.sidebar.selectbox(
        "Choose the feature selection method you want to see features' scores", available_feature_selection
    )

    # Loading features scores
    df_features_scores = load_scores_features(selected_feature_selection_method)

    # Sort features by score
    df_features_scores_sorted = df_features_scores.sort_values(by='feature_scores', ascending=False)

    return selected_feature_selection_method, df_features_scores_sorted


def plot_feature_selection_scores(selected_feature_selection_method, df_features_scores_sorted):
    
    # Selection of the number of feature to show
    number_features = st.sidebar.slider(
        "Select the number of features you want to see",
        min_value=1,
        max_value=200,
        value=20  # Default value
    )

    # Keep only the first lines
    df_features_scores_sorted_top = df_features_scores_sorted.head(number_features)

    # Colors for the plot bars
    colors = ['green' if selected == 1 else 'red' for selected in df_features_scores_sorted_top["feature_selected"]]

    # Create figure
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.bar(
        df_features_scores_sorted_top["feature_names"],
        df_features_scores_sorted_top["feature_scores"],
        color=colors,
    )
    ax.set_xlabel("Feature name", fontsize=12)
    ax.set_ylabel("Feature score", fontsize=12)
    ax.set_title(f"Feature importance for the feature selection {selected_feature_selection_method}", fontsize=16)

    # Adjust size
    ax.tick_params(axis="x", labelsize=12)
    ax.tick_params(axis="y", labelsize=12)
    # Ajust rotation
    plt.xticks(rotation=90, ha="right")
    # Adjust space
    plt.tight_layout()
    
    # Plot results
    st.pyplot(fig)    



############### Preloading (useless for the moment) ###############

############### Streamlit launch ###############

# Title and welcome message
welcome()

# Selection of the run and loading results of it
metrics_df, selected_experiment, selected_run_name = select_experiment()

# Visualize results of the run
#table_metrics_all(metrics_df)
plot_results_metric(metrics_df)

# Show config for this run
show_config(selected_experiment, selected_run_name)

# Selection of feature selection method and loading scores of the features
selected_feature_selection_method, df_features_scores_sorted = select_feature_selection_method()

# Visualize feature selection scores
plot_feature_selection_scores(selected_feature_selection_method, df_features_scores_sorted)
