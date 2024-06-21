import logging

import pandas as pd
from config import Config
from constants import Constants as C
from loaders import load_feature_library
from sklearn.feature_selection import VarianceThreshold
from tracking import write_selected_features
from utils import configure_main_logger

logger = logging.getLogger(__name__)


def select_all_features():
    logger.info("Select all features")
    df_feature_library = load_feature_library()
    selected_features = df_feature_library.columns.tolist()
    return selected_features

def select_above_variance_treshold_features():
    logger.info("Select features above a treshold for variance")
    df_feature_library = load_feature_library()
    selector = VarianceThreshold(threshold=Config.FEATURE_SELECTION_VARIANCE_TRESHOLD) 
    selector.fit(df_feature_library)
    selected_features = selector.get_feature_names_out()
    return selected_features

available_feature_selection = {
    "all": select_all_features,
    "variance": select_above_variance_treshold_features,
}

if __name__ == "__main__":
    logger = configure_main_logger("feature_selection")
    selected_features = available_feature_selection[
        Config.FEATURE_SELECTION_METHOD_NAME
    ]()
    write_selected_features(selected_features, Config.FEATURE_SELECTION_METHOD_NAME)
    logger.info("Features selected with success")
