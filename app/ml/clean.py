import os
import pandas as pd
from pathlib import Path

from app.ml.constants import Constants as C
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

def clean_study1_codebook():
    # Load the CSV
    df = pd.read_csv(C.CODEBOOK_PATH / "frozen_codebook_october_15.csv")

    # Filter out rows where id = -1
    df = df[df["id"] != -1]

    # Keep only the specified columns
    columns_to_keep = ["id", "bloc", "raw_variable_name", "raw_variable_type", "observability", "Questions", "Choix de réponse "]
    df = df[columns_to_keep]

    # Save the cleaned version
    df.to_csv("codebook_study1.csv", index=False)

    print("✅ codebook_study1.csv has been created successfully.")


def clean_merge_features():
    # Input 
    FEATURE_SELECTION_PATH = C.ML_PATH / 'real' / C.FEATURE_SELECTION_FOLDER_NAME / 'feature_library_v10'
    FEATURE_LIBARY_PATH = C.ML_PATH / 'real' / C.FEATURE_LIBRARIES_FOLDER_NAME / 'feature_library_v10'
    feature_selection_filename = C.FEATURE_SELECTION_FILENAME.format('xgboost_k_20')

    lookup_df = pd.read_csv(FEATURE_LIBARY_PATH / C.FEATURE_LOOKUP_FILENAME)
    selection_df = pd.read_csv(FEATURE_SELECTION_PATH / feature_selection_filename)

    # Merge on 'feature_names'
    merged_df = pd.merge(
        lookup_df,
        selection_df,
        on="feature_names",
        how="inner"  # only keep features present in both files
    )

    # Output
    data_shared_path = Path(os.getenv("DATA_SHARED_PATH"))
    study1_path = data_shared_path / "Study 1"
    merged_df.to_csv(study1_path / "features.csv", index=False)

    print("✅ merged_feature_data.csv created successfully.")
    print("Shape:", merged_df.shape)
