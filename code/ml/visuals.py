import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from config import Config
from loaders import load_results_metrics


def welcome():
    # Welcome
    st.write("Welcome on the visuals for Datagotchi Health")


def table_metrics_all():
    # Load metrics results
    metrics_df = load_results_metrics()

    # Show a table with all results
    st.write("Here is a table with all results")
    metrics_df


def plot_results_metric():

    # Load metrics results
    metrics_df = load_results_metrics()

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
table_metrics_all()
plot_results_metric()
