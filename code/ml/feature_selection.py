import logging

import numpy as np
import pandas as pd
from configs.score_feature import ScoreFeatureConfig as Config
from constants import Constants as C
from loaders import load_df_X_y

from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.feature_selection import SelectFromModel

from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBRegressor

from tracking import write_selected_features
from utils import configure_main_logger

logger = logging.getLogger(__name__)

# Score normalization
def score_normalization(feature_importances):
    feature_scores = (
        MinMaxScaler().fit_transform(feature_importances.reshape(-1, 1)).flatten()
    )
    return feature_scores

# Handle missing values
def missing_values(df_X, df_y):
    non_missing_indices = df_y.notna()
    df_y = df_y.loc[non_missing_indices]
    df_X = df_X.loc[non_missing_indices, :]
    df_X = df_X.fillna(df_X.mean())
    return df_X, df_y


# Feature selection selecting all features
def select_all_features(df_X, df_y):
    feature_names = df_X.columns
    feature_scores = [1.0] * len(feature_names)
    feature_selected = [1] * len(feature_names)
    return feature_selected, feature_scores


# Feature selection based on variance
def select_above_variance_treshold_features(df_X, df_y, threshold):
    logger.info(f"Select features above a treshold of {threshold} for variance")
    selector = VarianceThreshold(threshold)
    selector.fit(df_X)
    feature_variances = selector.variances_
    feature_selected = (feature_variances >= threshold).astype(int)

    # Normalize scores
    feature_scores = score_normalization(feature_variances)

    return feature_scores, feature_selected


# Feature selection based on k best features
def select_k_best_features(df_X, df_y, k):

    logger.info(f"Select {k} best features")

    # Selector
    selector = SelectKBest(score_func=f_regression, k=k)

    # Handle missing values
    df_X, df_y = missing_values(df_X, df_y)

    # Fit
    selector.fit_transform(df_X, df_y)

    feature_scores = selector.scores_
    threshold = np.partition(feature_scores, -k)[-k]
    feature_selected = (feature_scores >= threshold).astype(int)

    # Normalize scores
    feature_scores = score_normalization(feature_scores)

    return feature_scores, feature_selected


# Feature selection based on xgboost
def select_xgboost_features(df_X, df_y):
    logger.info(f"Select features based on xgboost")

    # Handle missing values
    df_X, df_y = missing_values(df_X, df_y)

    # Model xgboost
    model = XGBRegressor()
    model.fit(df_X, df_y)

    # Selector
    selector = SelectFromModel(model, threshold="mean")

    # Importance for features
    feature_importances = model.feature_importances_

    # Normalize scores
    feature_scores = score_normalization(feature_importances)

    # Selected features
    feature_selected = selector.get_support()

    return feature_scores, feature_selected



available_feature_selection = {
    "all": select_all_features,
    "variance": select_above_variance_treshold_features,
    "kbest": select_k_best_features,
    "xgboost": select_xgboost_features,
}

if __name__ == "__main__":
    logger = configure_main_logger("feature_selection")
    ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
    frozen_library_folder_name = Config.FEATURE_LIBRARY_VERSION
    df_X, df_y = load_df_X_y(
        ml_run_path / C.FEATURE_LIBRARIES_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_LIBRARY_FILENAME,
        C.TARGETS_FILENAME,
        eval(Config.TARGET_NAME),
    )
    method_name, method_params = Config.FEATURE_SELECTION_METHOD
    feature_selection_method = available_feature_selection[method_name]
    feature_scores, feature_selected = feature_selection_method(
        df_X, df_y, **method_params
    )
    write_selected_features(
        df_X.columns.tolist(),
        feature_scores,
        feature_selected,
        Config.FEATURE_SELECTION_METHOD,
        ml_run_path / C.FEATURE_SELECTION_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_SELECTION_FILENAME,
    )
    logger.info("Features selected with success")
