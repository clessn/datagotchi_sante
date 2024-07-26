from sklearn.impute import KNNImputer, SimpleImputer
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler


class DeployConfig:
    RUN_TYPE = "REAL_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME
    CODEBOOK_VERSION = "frozen_codebook_july_25.csv"

    # Best feature selection
    FEATURE_LIBRARY_VERSION = "feature_library_v6"
    FEATURE_SELECTION_METHOD = ("xgboost", {"k": 20})

    # Best Model
    BEST_MODEL = {
        "model_name": "xgboost_regressor",
        "param_grid": {
            "imputer": [SimpleImputer(strategy="mean"), KNNImputer()],
            "scaler": [StandardScaler(), MinMaxScaler()],
            "regressor__max_depth": [3, 6, 9],
            "regressor__subsample": [0.5, 0.8],
        }
    }
    MIN_TRAIN_SIZE = 30
    TARGET_NAME = "C.TARGET_SCORE_TOT"  # TARGET_SCORE_TOT, TARGET_POSITIVE_FUNCTIONING, TARGET_EMOTIONAL_HEALTH
    TARGET_BORNE_SUP = (
        70  # 70 for score_tot, 55 for positive_functioning, 15 for emotional_health
    )
    KFOLD_HP = 3


    # Example generation
    N_USERS = 3
