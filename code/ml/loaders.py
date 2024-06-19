import pandas as pd
from config import Config
from constants import Constants as C


def explore_raw_data():
    df_str = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME, convert_categoricals=True)
    df_num = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME, convert_categoricals=False)
    return df_str, df_num


def load_codebook():
    df = pd.read_csv(C.ML_ROOT_PATH / C.CODEBOOK_FILENAME)
    return df.loc[:, C.CODEBOOK_COLS].drop_duplicates()


def load_attributes():
    df = pd.read_csv(C.ML_PATH / C.ATTRIBUTES_FILENAME)
    df = df.set_index(C.ATTRIBUTE_ID_COL)
    return df


def load_feature_library():
    df_feature_library = pd.read_csv(
        C.FEATURE_LIBRARY_VERSION_PATH / C.FEATURE_LIBRARY_FILENAME,
        index_col=C.ATTRIBUTE_ID_COL,
    )
    return df_feature_library

def load_targets():
    df_targets = pd.read_csv(
        C.FEATURE_LIBRARY_VERSION_PATH / C.TARGETS_FILENAME,
        index_col=C.ATTRIBUTE_ID_COL,
    )
    return df_targets

def load_selected_features(method_name):
    """
    Reads a file containing selected features, one per line, and returns a list of these features.
    
    :param method_name: The name of the feature selection method to consider. 
    :return: A list of selected features.
    """
    features = []
    with open(C.FEATURE_SELECTION_PATH / C.FEATURE_SELECTION_FILENAME.format(method_name), 'r') as file:
        features = [line.strip() for line in file]
    return features


def load_features_target():
    df_feature_library = load_feature_library()
    df_targets = load_targets()
    assert df_feature_library.index.equals(df_targets.index)
    selected_features = load_selected_features(Config.FEATURE_SELECTION_METHOD_NAME)
    X = df_feature_library[selected_features].values
    y = df_targets[eval(Config.TARGET_NAME)].values
    return X, y


def load_results_metrics():
    metrics_df = pd.read_csv(C.ML_PATH / C.METRICS_FILENAME)
    return metrics_df
