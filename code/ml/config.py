class Config:
    # Config variables
    kfold = 5
    model_list = [(baseline_mean_regressor, "Baseline Mean Regression", {}), 
                  (baseline_random_regressor, "Baseline Random Regression", {})]
    target_list = [score_total]
    metric_list = [MSE]

