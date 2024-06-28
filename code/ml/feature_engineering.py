import logging

import numpy as np
import pandas as pd
from constants import Constants as C
from configs.create_feature import CreateFeatureConfig as Config
from loaders import load_attributes, load_codebook
from tracking import write_feature_library
from utils import configure_main_logger

logger = logging.getLogger(__name__)


def features_in_codebook_and_attributes(fields, df_codebook, df_attributes):
    codebook_fields_variables = df_codebook.loc[
        df_codebook[C.CODEBOOK_TYPE_COL].isin(fields), C.CODEBOOK_NAME_COL
    ].values
    codebook_fields_attributes_variables = [
        variable
        for variable in codebook_fields_variables
        if variable in df_attributes.columns
    ]
    return codebook_fields_attributes_variables


def create_nominal_multiple_features(df_codebook, df_attributes):

    # Select nominal_multiple_features
    nominal_multiple_fields = [
        C.CODEBOOK_TYPE_NOMINAL_MULTIPLE_LABEL,
    ]

    nominal_multiple_variables_in_attributes = features_in_codebook_and_attributes(
        nominal_multiple_fields, df_codebook, df_attributes
    )
    logger.info(
        f"{len(nominal_multiple_variables_in_attributes)} variables are nominal multiple."
    )

    # Keep only those columns
    df_nominal_multiple_features = df_attributes[
        nominal_multiple_variables_in_attributes
    ].copy()

    # Convert '1.0' into 1 and Nan into 0
    df_nominal_multiple_features = df_nominal_multiple_features.fillna(0).astype(int)
    return df_nominal_multiple_features


def create_nominal_single_features(df_codebook, df_attributes):

    # Select nominal_single_features
    nominal_single_fields = [
        C.CODEBOOK_TYPE_NOMINAL_SINGLE_LABEL,
    ]
    nominal_single_variables_in_attributes = features_in_codebook_and_attributes(
        nominal_single_fields, df_codebook, df_attributes
    )

    # Keep only those columns
    df_nominal_single_features = df_attributes[
        nominal_single_variables_in_attributes
    ].copy()

    # Convert it into dummies (one-hot encoding)
    # TODO: Take categories from codebook (num, not text), assert values are in categories, add the categories in getdummies
    df_nominal_single_features = pd.get_dummies(
        df_nominal_single_features,
        columns=nominal_single_variables_in_attributes,
        dtype=int,
    )
    logger.info(
        f"{len(nominal_single_variables_in_attributes)} variables are nominal single and are converted into {len(df_nominal_single_features.columns)} variables one-hot encoded."
    )
    return df_nominal_single_features


def create_numerical_features(df_codebook, df_attributes):
    numerical_fields = [
        C.CODEBOOK_TYPE_INTEGER_LABEL,
        C.CODEBOOK_TYPE_FLOAT_LABEL,
        C.CODEBOOK_TYPE_ORDINAL_LABEL,
    ]
    numerical_variables_in_attributes = features_in_codebook_and_attributes(
        numerical_fields, df_codebook, df_attributes
    )
    logger.info(f"{len(numerical_variables_in_attributes)} variables are numerical.")
    return df_attributes.loc[:, numerical_variables_in_attributes]


def keep_observable(df_codebook, df_attributes):
    df_codebook_observable = df_codebook[
        df_codebook[C.CODEBOOK_OBSERVABILITY_COL].isin(C.OBSERVABILITY_LEVEL)
    ].copy()
    observables_variables = df_codebook_observable[C.CODEBOOK_NAME_COL].values
    observables_variables_in_attributes = [
        variable
        for variable in observables_variables
        if variable in df_attributes.columns
    ]
    df_attributes_observable = df_attributes[observables_variables_in_attributes]
    logger.info(
        f"Before the observability step, {df_attributes.shape[1]} variables were available. After the observability step, {df_attributes_observable.shape[1]} variables are kept."
    )
    return df_attributes_observable


# Run feature_engineering
if __name__ == "__main__":
    logger = configure_main_logger("feature_engineering")
    ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")

    # Load codebook and attributes
    df_codebook = load_codebook(C.CODEBOOK_PATH, Config.CODEBOOK_VERSION)
    df_attributes = load_attributes(ml_run_path, C.ATTRIBUTES_FILENAME)

    # Targets
    df_targets = df_attributes.loc[:, C.TARGET_COLS]

    # Candidates attributes, removing targets
    df_candidate = df_attributes.drop(columns=C.TARGET_COLS)

    # Observable variables
    df_candidate_observable = keep_observable(df_codebook, df_candidate)

    # Numerical features
    df_numerical_features = create_numerical_features(
        df_codebook, df_candidate_observable
    )

    # Nominal single features, one-hot encoded
    df_nominal_single_features = create_nominal_single_features(
        df_codebook, df_candidate_observable
    )

    # Nominal multiple features
    df_nominal_multiple_features = create_nominal_multiple_features(
        df_codebook, df_candidate_observable
    )

    # Aggregate here different type of features
    df_features = pd.concat(
        [
            df_numerical_features,
            df_nominal_single_features,
            df_nominal_multiple_features,
        ],
        axis=1,
    )

    # Save features and targets to csv
    write_feature_library(
        df_features,
        df_targets,
        ml_run_path / C.FEATURE_LIBRARIES_FOLDER_NAME,
        C.FEATURE_LIBRARY_FILENAME,
        C.TARGETS_FILENAME,
    )
    logger.info("Features and Targets created with success !! :-)")
