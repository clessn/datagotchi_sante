import logging
from pathlib import Path

from constants import Constants as C

logger = logging.getLogger(__name__)

def write_feature_library(df_features, df_targets):
    df_features.to_csv(C.FEATURE_LIBRARIES_PATH / C.FEATURE_LIBRARY_FILENAME)
    df_targets.to_csv(C.FEATURE_LIBRARIES_PATH / C.TARGETS_FILENAME)
    logger.info('Feature library saved with targets')


def write_selected_features(selected_features, method_name):
    Path(C.FEATURE_SELECTION_PATH).mkdir(parents=True, exist_ok=True)
    with open(C.FEATURE_SELECTION_PATH / C.FEATURE_SELECTION_FILENAME.format(method_name), "w") as f:
        for feature in selected_features:
            f.write(feature +"\n")


def track_results(metrics_df, predictions_df):
    pass