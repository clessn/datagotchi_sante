import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from configs.visuals import VisualsConfig as Config
from constants import Constants as C
from feature_selection import available_feature_selection
from loaders import load_config, load_results_metrics, load_scores_features


def welcome():
    # Welcome
    st.title("Visuals for Datagotchi Health")


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


def table_metrics_all(metrics_df):

    # Show a table with all results
    st.write("Here is a table with all results")
    metrics_df[["fold_id", "model_name", "metric_name", "metric_value"]]


def plot_results_metric(metrics_df):

    # Select a metric

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


def select_feature_selection_method(feature_selection_path):

    # Title of sidebar
    st.sidebar.title("Feature selection")

    # Available feature selection methods
    prefix = C.FEATURE_SELECTION_FILENAME.split("{}")[0]
    suffix = C.FEATURE_SELECTION_FILENAME.split("{}")[1]
    available_feature_selection = [feature_selection_method.replace(prefix, "").replace(suffix, "") for feature_selection_method in os.listdir(feature_selection_path)]
    
    # Put it in a dictionnary
    selection_methods_dict = {}
    for feature_selection_method in available_feature_selection:
        feature_selection_method_parts = feature_selection_method.split("_")
        method_name = feature_selection_method_parts[0]
        param_dict = {}        
        if len(feature_selection_method_parts)>2:
            param_dict = {feature_selection_method_parts[i]: feature_selection_method_parts[i+1] for i in range(1, len(feature_selection_method_parts), 2)}
        selection_methods_dict[feature_selection_method] = (method_name,param_dict)
    
    # List with feature selection methods
    unique_methods_list = list({method[0] for method in selection_methods_dict.values()})
    
    # Selection of the feature selection method
    selected_feature_selection_method = st.sidebar.selectbox(
        "Choose the feature selection method you want to see features' scores",
        unique_methods_list,
    )

    # Available parameters for this feature selection method
    feature_selection_parameters = {}
    for feature_selection_method in selection_methods_dict:
        feature_selection_method_name, feature_selection_method_param = selection_methods_dict[feature_selection_method]
        if feature_selection_method_name == selected_feature_selection_method and len(feature_selection_method_param)>0:
            feature_selection_parameters[feature_selection_method] = feature_selection_method_param
    
    # Selection the parameters for the feature selection
    selected_feature_selection_method_parameters = {}
    if len(feature_selection_parameters)>0:
        selected_feature_selection_method_parameters_name = st.sidebar.selectbox(
            "Choose the feature selection method you want to see features' scores",
            feature_selection_parameters,
        )
        selected_feature_selection_method_parameters = feature_selection_parameters[selected_feature_selection_method_parameters_name]

    # Loading features scores
    df_features_scores = load_scores_features(
        (selected_feature_selection_method,selected_feature_selection_method_parameters),
        feature_selection_path,
        C.FEATURE_SELECTION_FILENAME,
    )
    
    # Sort features by score
    df_features_scores_sorted = df_features_scores.sort_values(
        by="feature_scores", ascending=False
    )

    return selected_feature_selection_method, df_features_scores_sorted


def plot_feature_selection_scores(
    selected_feature_selection_method, df_features_scores_sorted
):

    # Selection of the number of feature to show
    number_features = st.sidebar.slider(
        "Select the number of features you want to see",
        min_value=1,
        max_value=200,
        value=20,  # Default value
    )

    # Keep only the first lines
    df_features_scores_sorted_top = df_features_scores_sorted.head(number_features)

    # Map feature_selected values to labels for legend
    df_features_scores_sorted_top["selected_label"] = df_features_scores_sorted_top[
        "feature_selected"
    ].apply(lambda x: "selected" if x == 1 else "not selected")

    # Create plot using plotly
    fig = px.bar(
        df_features_scores_sorted_top,
        x="feature_names",
        y="feature_scores",
        color="selected_label",
        color_discrete_map={"selected": "green", "not selected": "red"},
        labels={"feature_names": "Feature name", "feature_scores": "Feature score"},
        title=f"Feature importance for the feature selection {selected_feature_selection_method}",
    )

    # Rotate x-axis labels
    fig.update_layout(xaxis_tickangle=-90)

    # Plot results
    st.plotly_chart(fig)


############### Preloading (useless for the moment) ###############

# Derive paths from configs
ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
experiments_path = ml_run_path / C.EXPERIMENTS_FOLDER_NAME
frozen_library_folder_name = Config.FEATURE_LIBRARY_VERSION
feature_selection_path = ml_run_path / C.FEATURE_SELECTION_FOLDER_NAME / frozen_library_folder_name


############### Streamlit launch ###############

# Title and welcome message
welcome()

# Selection of the run and loading results of it
metrics_df, selected_experiment, selected_run_name = select_experiment(experiments_path)

# Select a metric and visualize results of the run
# table_metrics_all(metrics_df)
plot_results_metric(metrics_df)

# Selection of feature selection method and loading scores of the features
selected_feature_selection_method, df_features_scores_sorted = (
    select_feature_selection_method(feature_selection_path)
)

# Visualize feature selection scores
plot_feature_selection_scores(
    selected_feature_selection_method, df_features_scores_sorted
)

# Show config for this run
show_config(experiments_path, selected_experiment, selected_run_name)

