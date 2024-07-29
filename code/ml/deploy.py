import argparse
import logging

import numpy as np
import pandas as pd
from configs.deploy import DeployConfig as Config
from constants import Constants as C
from crossval import preallocate_pipeline, scaling_y
from feature_engineering import create_features
from loaders import (
    load_attributes,
    load_best_model,
    load_codebook,
    load_df_X_y,
    load_feature_lookup_table,
    load_selected_features,
)
from sklearn.model_selection import GridSearchCV
from tracking import save_example_predictions, write_best_model, write_example
from utils import configure_main_logger

logger = logging.getLogger(__name__)


# Create questionnaire
def create_questionnaire(
    df_feature_lookup,
    selected_features,
    df_codebook,
):
    questions = (
        df_feature_lookup.loc[
            df_feature_lookup[C.LOOKUP_FEATURE_NAME_COL].isin(selected_features),
            C.CODEBOOK_NAME_COL,
        ]
        .unique()
        .tolist()
    )
    df_questionnaire = df_codebook.loc[
        df_codebook[C.CODEBOOK_NAME_COL].isin(questions),
        [
            C.CODEBOOK_ID_COL,
            C.CODEBOOK_NAME_COL,
            C.CODEBOOK_QUESTION_COL,
            C.CODEBOOK_CHOICE_COL,
        ],
    ]
    df_questionnaire = df_questionnaire.drop_duplicates(C.CODEBOOK_ID_COL)

    return df_questionnaire


def create_example(df_attributes, raw_variable_names):
    df_users = df_attributes.sample(n=Config.N_USERS, random_state=42)[
        raw_variable_names
    ]
    df_users.index = range(Config.N_USERS)
    df_users.index.name = C.ATTRIBUTE_ID_COL
    return df_users


def generate_questionnaire_and_example(ml_run_path, frozen_library_folder_name):

    # Load codebook
    df_codebook = load_codebook(C.CODEBOOK_PATH, Config.CODEBOOK_VERSION)

    # Load feature lookup-table
    df_feature_lookup = load_feature_lookup_table(
        ml_run_path / C.FEATURE_LIBRARIES_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_LOOKUP_FILENAME,
    )

    # Load selected feature
    selected_features = load_selected_features(
        Config.FEATURE_SELECTION_METHOD,
        ml_run_path / C.FEATURE_SELECTION_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_SELECTION_FILENAME,
    )

    # Create questionnaire
    df_questionnaire = create_questionnaire(
        df_feature_lookup,
        selected_features,
        df_codebook,
    )

    # Create example
    df_attributes = load_attributes(ml_run_path, C.ATTRIBUTES_FILENAME)
    df_example = create_example(
        df_attributes, df_questionnaire[C.CODEBOOK_NAME_COL].tolist()
    )

    write_example(
        df_questionnaire,
        df_example,
        ml_run_path / C.DEPLOY_FOLDER_NAME,
        C.QUESTIONNAIRE_FILENAME,
        C.EXAMPLE_ANSWERS_FILENAME,
    )


def train_best_model(ml_run_path, frozen_library_folder_name):
    # Load data
    df_X, df_y = load_df_X_y(
        ml_run_path / C.FEATURE_LIBRARIES_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_LIBRARY_FILENAME,
        C.TARGETS_FILENAME,
        eval(Config.TARGET_NAME),
    )
    selected_features = load_selected_features(
        Config.FEATURE_SELECTION_METHOD,
        ml_run_path / C.FEATURE_SELECTION_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_SELECTION_FILENAME,
    )
    df_X_selected = df_X.loc[:, selected_features]

    # Prepare X_train and y_train
    X_train = df_X_selected.values
    y_train = df_y.values
    y_train = scaling_y(y_train, Config.TARGET_BORNE_SUP)

    indices_nan_y_train = np.isnan(y_train)
    assert sum(~indices_nan_y_train) >= Config.MIN_TRAIN_SIZE

    # Remove y_train missing
    y_train = y_train[~indices_nan_y_train]
    X_train = X_train[~indices_nan_y_train]

    # Prepare a pipeline
    model_name = Config.BEST_MODEL["model_name"]
    param_grid = Config.BEST_MODEL["param_grid"]
    logger.info(f"Training for: {model_name}")
    pipeline = preallocate_pipeline(model_name, param_grid)

    # Perform HP optimization
    grid_search = GridSearchCV(pipeline, param_grid, cv=Config.KFOLD_HP)
    logger.debug(
        f"Performing hyperparameter optimization with {Config.KFOLD_HP} splits"
    )
    grid_search.fit(X_train, y_train)

    # Fit the best model
    logger.debug(
        f"- Fitting with: {grid_search.best_params_}",
    )
    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train)
    best_hyperparameters = grid_search.best_params_
    best_hyperparameters["model_name"] = model_name

    write_best_model(
        best_model,
        selected_features,
        grid_search.best_params_,
        ml_run_path / C.DEPLOY_FOLDER_NAME,
        C.BEST_MODEL_FILENAME,
        C.BEST_PARAMS_FILENAME,
    )


def create_features_for_example(df_attributes_example, ml_run_path):
    df_attributes = load_attributes(ml_run_path, C.ATTRIBUTES_FILENAME)
    df_codebook = load_codebook(C.CODEBOOK_PATH, Config.CODEBOOK_VERSION)
    assert all([col in df_attributes for col in df_attributes_example])
    df_attributes_with_example = pd.concat(
        (df_attributes[df_attributes_example.columns], df_attributes_example),
        axis=0,
    )
    df_features, _ = create_features(df_attributes_with_example, df_codebook)
    return df_features.iloc[-df_attributes_example.shape[0] :, :]


def predict_for_example(ml_run_path, frozen_library_folder_name):
    df_attributes_example = pd.read_csv(
        ml_run_path / C.DEPLOY_FOLDER_NAME / C.EXAMPLE_ANSWERS_FILENAME
    ).set_index(C.ATTRIBUTE_ID_COL)
    df_features_example = create_features_for_example(
        df_attributes_example, ml_run_path
    )

    best_model, selected_features = load_best_model(
        ml_run_path / C.DEPLOY_FOLDER_NAME,
        C.BEST_MODEL_FILENAME,
    )
    assert all(col in df_features_example.columns for col in selected_features)
    X = df_features_example[selected_features].values
    y = best_model.predict(X)
    df_y = pd.DataFrame(
        y,
        index=df_features_example.index,
        columns=[f"{eval(Config.TARGET_NAME)}_prediction"],
    )
    save_example_predictions(
        df_y,
        ml_run_path / C.DEPLOY_FOLDER_NAME,
        C.EXAMPLE_PREDICTION_FILENAME,
    )


# Run deploy
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deploy script")
    parser.add_argument("function", type=str, help="Function to execute")

    args = parser.parse_args()

    logger = configure_main_logger("deploy")

    ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
    frozen_library_folder_name = Config.FEATURE_LIBRARY_VERSION

    if args.function == "generate_questionnaire_and_example":
        generate_questionnaire_and_example(
            ml_run_path,
            frozen_library_folder_name,
        )
    elif args.function == "train_best_model":
        train_best_model(
            ml_run_path,
            frozen_library_folder_name,
        )
    elif args.function == "predict_for_example":
        predict_for_example(
            ml_run_path,
            frozen_library_folder_name,
        )
    else:
        print(f"Function {args.function} not recognized")
