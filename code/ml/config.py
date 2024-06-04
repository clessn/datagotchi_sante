from constants import Constants as C
from metrics import MSE
from models import MeanRegressor, RandomValueRegressor


class Config:
    # Config variables
    KFOLD = 5
    MODEL_LIST = [
        (MeanRegressor, "mean_regressor", {}),
        (RandomValueRegressor, "random_regressor", {}),
    ]
    TARGET_NAME = C.TARGET_SCORE_TOT
    METRIC_LIST = [MSE]

    # Random state
    RANDOM_STATE = 42
