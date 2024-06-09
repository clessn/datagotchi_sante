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
    MODEL_LIST = [
        "mean_regressor",
        "random_regressor",
        "linear_regressor",
        "extra_tree_regressor",
    ]
    TARGET_NAME = "C.TARGET_SCORE_TOT"

    # 2. Sandbox creation
    SANDBOX_N_ATTRIBUTES = 20
    SANDBOX_N_SAMPLE = 200
    SANDBOX_RANDOM_STATE = 42
