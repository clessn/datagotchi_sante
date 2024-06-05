import numpy as np
import pandas as pd
import streamlit as st

from config import Config
from loaders import load_results_metrics

def welcome():
    # Welcome
    st.write("Welcome on the visuals for Datagotchi Health")

def plot_results_metric():

    # Load metrics results
    metrics_df = load_results_metrics()

    # Show a table with all results
    metrics_df

    # Select a metric
    metric_choice = st.selectbox(
        'Which metric do you want to plot?',
        Config.METRIC_LIST)

    # Keep only results for this metric
    selected_metric_df = metrics_df[metrics_df['metric_name'] == metric_choice].copy()
    selected_metric_df

    # Group by model
    mean_selected_metric_df = selected_metric_df.groupby('model_name')['metric_value'].mean()
    mean_selected_metric_df

    # Plot results
    st.line_chart(mean_selected_metric_df)


welcome()
plot_results_metric()