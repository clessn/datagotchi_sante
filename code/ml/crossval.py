import pandas as pd
import numpy as np

from config import Config as Config
from constants import Constants as C
from loaders import load_features_target
from metrics import available_metrics_dict
from models import available_models_dict
from sklearn.model_selection import KFold

# Filling missing values in X
def fill_nan_with_value(X, values):
    indices_nan = np.where(np.isnan(X))
    X[indices_nan] = np.take(values, indices_nan[1])
    return X


def crossval(X, y):
    """Cross-validation (evaluation realized for each fold of each model)

    Attributes
    ----------
    - X : a numpy array containing the features
    - y : a vector containing the target

    Returns
    -------
    """

    # Split in folds
    kf = KFold(n_splits=Config.KFOLD, shuffle=True, random_state=Config.RANDOM_STATE_SPLITTING)

    # Lists for predictions results
    fold_id_predict_list = []
    model_name_predict_list = []
    y_test_list = []
    y_predict_list = []

    # Lists for metrics results
    fold_id_metric_list = []
    model_name_metric_list = []
    metric_name_list = []
    metric_value_list = []

    # Loop on folds
    for fold_index, (train_index, test_index) in enumerate(kf.split(X)):

        # Variables X,y train and test
        X_train = X[train_index, :].copy()
        X_test = X[test_index, :].copy()
        y_train = y[train_index].copy()
        y_test = y[test_index].copy()

        # Mean of values for X_train
        mu_X_train = np.nanmean(X_train, axis=0)

        # Replace missing values in X_test
        X_train = fill_nan_with_value(X_train, mu_X_train)
        X_test = fill_nan_with_value(X_test, mu_X_train)

        # Assert minimal number of targets
        indices_nan_y_train = np.isnan(y_train)
        assert sum(~indices_nan_y_train) >= Config.MIN_TRAIN_SIZE

        # Remove y_train missing
        y_train = y_train[~indices_nan_y_train]
        X_train = X_train[~indices_nan_y_train]
        
        # Loop on models
        for model_name, model_param in Config.MODEL_LIST:

            # Model class
            model_class = available_models_dict[model_name]

            # Instanciate model
            model = model_class(**model_param)

            # Fit the model
            model.fit(X_train, y_train)

            # Predict
            y_predict = model.predict(X_test)

            # Add prediction to lists
            fold_id_predict_list += [fold_index] * len(y_test)
            model_name_predict_list += [model_name] * len(y_test)
            y_test_list += y_test.tolist()
            y_predict_list += y_predict.tolist()

            # Parameters y for metrics
            metric_param_y = {
                "y_true": y_test,
                "y_pred": y_predict,
            }

            # Loop on metric
            for metric_name, metric_param in Config.METRIC_LIST:

                # Metric function
                metric_function = available_metrics_dict[metric_name]

                # Parameters for metric
                metric_param_extended = {**metric_param_y, **metric_param}
                metric_value = metric_function(**metric_param_extended)

                # Add metric to lists
                fold_id_metric_list.append(fold_index)
                model_name_metric_list.append(model_name)
                metric_name_list.append(metric_name)
                metric_value_list.append(metric_value)

    # Dict for predictions results
    predictions_dict = {
        "fold_id": fold_id_predict_list,
        "model_name": model_name_predict_list,
        "y_test": y_test_list,
        "y_predict": y_predict_list,
    }
    predictions_df = pd.DataFrame.from_dict(predictions_dict)

    # Dict for metrics results
    metrics_dict = {
        "fold_id": fold_id_metric_list,
        "model_name": model_name_metric_list,
        "metric_name": metric_name_list,
        "metric_value": metric_value_list,
    }
    metrics_df = pd.DataFrame.from_dict(metrics_dict)

    # To csv
    predictions_df.to_csv(C.ML_PATH / C.PREDICTIONS_SANDBOX_FILENAME)
    metrics_df.to_csv(C.ML_PATH / C.METRICS_SANDBOX_FILENAME)


# Load data
X, y = load_features_target()
crossval(X, y)
