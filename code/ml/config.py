class Config:

    # 1. Predictions
    # 1.1. Run type
    RUN_TYPE = "SANDBOX_FOLDER_NAME"  # SANDBOX_FOLDER_NAME or REAL_FOLDER_NAME

    # 1.2. Evaluation
    KFOLD = 5
    METRIC_LIST = [
        "mse",
        "mae",
    ]
    MIN_TRAIN_SIZE = 30
    MIN_TEST_SIZE = 30
    RANDOM_STATE_SPLITTING = 42

    # 1.3. Modelling
    MODEL_MEAN_REGRESSOR_NAME = "mean_regressor"
    MODEL_RANDOM_REGRESSOR_NAME = "random_regressor"
    MODEL_LINEAR_REGRESSOR_NAME = "linear_regressor"
    MODEL_EXTRA_TREE_REGRESSOR_NAME = "extra_tree_regressor"
    MODEL_LIST = [
        MODEL_MEAN_REGRESSOR_NAME,
        MODEL_RANDOM_REGRESSOR_NAME,
        MODEL_LINEAR_REGRESSOR_NAME,
        MODEL_EXTRA_TREE_REGRESSOR_NAME,
    ]
    TARGET_NAME = "C.TARGET_SCORE_TOT"
    SCALER_CHOICE = {
        MODEL_LINEAR_REGRESSOR_NAME: "minmax",
        MODEL_EXTRA_TREE_REGRESSOR_NAME: "std",
    }
    IMPUTER_CHOICE = {
        MODEL_LINEAR_REGRESSOR_NAME: "imputer_mean",
        MODEL_EXTRA_TREE_REGRESSOR_NAME: "imputer_mean",
    }

    # 2. Sandbox creation
    SANDBOX_N_ATTRIBUTES = 20
    SANDBOX_N_SAMPLE = 200
    SANDBOX_RANDOM_STATE = 42
