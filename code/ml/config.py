class Config:
    # Config variables
    KFOLD = 5
    MODEL_LIST = [
        (MeanRegressor, "Mean Regressor", {}),
        (RandomRegressor, "Random Regressor", {}),
    ]
    TARGET_LIST = [score_total]
    METRIC_LIST = [MSE]

    # Random state
    RANDOM_STATE = 42
