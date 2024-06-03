from constants import Constants as C
from metrics import MSE
from models import MeanRegressor
from models import RandomValueRegressor

class Config:
    # Config variables
    KFOLD = 5
    MODEL_LIST = [
        (MeanRegressor, "Mean Regressor", {}),
        (RandomValueRegressor, "Random Regressor", {}),
    ]
    TARGET_LIST = [C.SCORE_TOT]
    METRIC_LIST = [MSE]

    # Random state
    RANDOM_STATE = 42
