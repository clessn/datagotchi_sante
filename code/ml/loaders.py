import json
import pandas as pd
from constants import Constants as C


def explore_raw_data(path, filename):
    df_str = pd.read_spss(path / filename, convert_categoricals=True)
    df_num = pd.read_spss(path / filename, convert_categoricals=False)
    return df_str, df_num


def load_codebook(path, filename):
    df = pd.read_csv(path / filename)
    return df.loc[:, C.CODEBOOK_COLS].drop_duplicates()


def load_attributes(path, filename):
    df = pd.read_csv(path / filename)
    df = df.set_index(C.ATTRIBUTE_ID_COL)
    return df


def load_feature_library(path, filename):
    df_feature_library = pd.read_csv(
        path / filename,
        index_col=C.ATTRIBUTE_ID_COL,
    )
    return df_feature_library


def load_targets(path, filename):
    df_targets = pd.read_csv(
        path / filename,
        index_col=C.ATTRIBUTE_ID_COL,
    )
    return df_targets


def load_df_X_y(path, feature_library_filename, targets_filename, target_name):
    df_feature_library = load_feature_library(path, feature_library_filename)
    df_targets = load_targets(path, targets_filename)
    assert df_feature_library.index.equals(df_targets.index)
    return df_feature_library, df_targets[target_name]


def load_selected_features(method_name):
    """
    Reads a file containing selected features, one per line, and returns a list of these features.

    :param method_name: The name of the feature selection method to consider.
    :return: A list of selected features.
    """
    df_selected = pd.read_csv(
        C.FEATURE_SELECTION_PATH / C.FEATURE_SELECTION_FILENAME.format(method_name)
    )
    selected_features = df_selected.loc[
        df_selected["feature_selected"] == 1, "feature_names"
    ].tolist()
    return selected_features



def load_results_metrics(experiment_name):
    experiments_version_path = C.EXPERIMENTS_PATH / experiment_name
    metrics_df = pd.read_csv(experiments_version_path / C.METRICS_FILENAME)
    return metrics_df

def load_config(config_path):
    # Opening JSON file
    config_file = open(config_path / C.ARTIFACTS_CONFIG_FILENAME)
    config_df = json.load(config_file)
    return config_df
