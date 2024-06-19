import logging
import pandas as pd
from constants import Constants as C
from utils import configure_main_logger
from loaders import load_feature_library
from config import Config
from tracking import write_selected_features

logger = logging.getLogger(__name__)


def select_all_features():
    logger.info('Select all features')
    df_feature_library = load_feature_library()
    selected_features = df_feature_library.columns.tolist()
    return selected_features


available_feature_selection = {
    'all': select_all_features,
}

if __name__ == "__main__":
    logger = configure_main_logger("feature_selection")
    selected_features = available_feature_selection[Config.FEATURE_SELECTION_METHOD_NAME]()
    write_selected_features(selected_features, Config.FEATURE_SELECTION_METHOD_NAME)
    logger.info('Features selected with success')


    

