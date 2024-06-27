import logging

import pandas as pd
from config import Config
from constants import Constants as C
from loaders import load_feature_library, load_targets
from sklearn.feature_selection import SelectKBest, VarianceThreshold, f_regression
from tracking import write_selected_features
from utils import configure_main_logger

logger = logging.getLogger(__name__)


def select_all_features():
    logger.info("Select all features")
    df_feature_library = load_feature_library()
    selected_features = df_feature_library.columns.tolist()
    return selected_features


def select_above_variance_treshold_features():
    logger.info(
        f"Select features above a treshold of {Config.FEATURE_SELECTION_VARIANCE_TRESHOLD} for variance"
    )
    df_feature_library = load_feature_library()
    selector = VarianceThreshold(threshold=Config.FEATURE_SELECTION_VARIANCE_TRESHOLD)
    selector.fit(df_feature_library)
    selected_features = selector.get_feature_names_out()
    return selected_features


# Unsupervised feature selection, should be adapted later for using it
def select_k_best_features():
    logger.info(f"Select {Config.FEATURE_SELECTION_K_BEST} best features")
    df_feature_library = load_feature_library()
    df_targets = load_targets()
    selector = SelectKBest(score_func=f_regression, k=Config.FEATURE_SELECTION_K_BEST)
    selector.fit_transform(df_feature_library, df_targets)
    selected_features = selector.get_feature_names_out()
    return selected_features


available_feature_selection = {
    "all": select_all_features,
    "variance": select_above_variance_treshold_features,
    # "kbest": select_k_best_features,
}

if __name__ == "__main__":
    logger = configure_main_logger("feature_selection")
    selected_features = available_feature_selection[
        Config.FEATURE_SELECTION_METHOD_NAME
    ]()
    write_selected_features(selected_features, Config.FEATURE_SELECTION_METHOD_NAME)
    logger.info("Features selected with success")
