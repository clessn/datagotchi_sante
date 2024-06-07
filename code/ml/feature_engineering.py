import logging
import numpy as np
import pandas as pd

from constants import Constants as C
from loaders import load_attributes, load_codebook
from utils import configure_main_logger

logger = logging.getLogger(__name__)

def create_numerical_features(df_attributes):
    numerical_fields = [
        C.CODEBOOK_TYPE_INTEGER_LABEL,
        C.CODEBOOK_TYPE_FLOAT_LABEL,
        C.CODEBOOK_TYPE_ORDINAL_LABEL,
    ]
    numerical_variables = df_codebook.loc[
        df_codebook[C.CODEBOOK_TYPE_COL].isin(numerical_fields), C.CODEBOOK_NAME_COL
    ].values
    numerical_variables_in_attributes = [variable for variable in numerical_variables if variable in df_attributes.columns]
    return df_attributes.loc[:, numerical_variables_in_attributes]

def keep_observable(df_codebook, df_attributes):
    df_codebook_observable = df_codebook[df_codebook[C.CODEBOOK_OBSERVABILITY_COL].isin(C.OBSERVABILITY_LEVEL)].copy()
    observables_variables = df_codebook_observable[C.CODEBOOK_NAME_COL].values
    observables_variables_in_attributes = [variable for variable in observables_variables if variable in df_attributes.columns]
    df_attributes_observable = df_attributes[observables_variables_in_attributes]
    return df_attributes_observable

# Run feature_engineering
if __name__ == "__main__":
    logger = configure_main_logger("feature_engineering")

    # Load codebook and attributes
    df_codebook = load_codebook()
    df_attributes = load_attributes()

    # Targets
    df_targets = df_attributes.loc[:, C.TARGET_COLS]

    # Candidates attributes, removing targets
    df_candidate = df_attributes.drop(columns=C.TARGET_COLS)

    # Observable variables
    df_candidate_observable = keep_observable(df_codebook, df_candidate)

    # Numerical features
    df_numerical_features = create_numerical_features(df_candidate_observable)

    # Aggregate here different type of features
    df_features = df_numerical_features  

    # Save features and targets to csv
    df_features.to_csv(C.ML_PATH / C.FEATURES_FILENAME)
    df_targets.to_csv(C.ML_PATH / C.TARGETS_FILENAME)
    logger.info("Features and Targets created with success !! :-)")
