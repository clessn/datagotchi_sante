from app.ml.constants import Constants as C
from app.ml.configs.eda import EdaConfig as Config
from app.ml.loaders import load_targets

def score_eda():
    ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
    frozen_library_folder_name = Config.FEATURE_LIBRARY_VERSION
    df_y = load_targets(
        ml_run_path / C.FEATURE_LIBRARIES_FOLDER_NAME / frozen_library_folder_name, 
        C.TARGETS_FILENAME,
    )
    print(df_y)