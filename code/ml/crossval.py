from sklearn.model_selection import KFold
import pandas as pd

from constants import Constants as C
from config import Config as Config
from loaders import load_features_target
from metrics import metrics_dict
from models import models_dict


def crossval(X, y):
    """Cross-validation (evaluation realized for each fold of each model)

    Attributes
    ----------
    - X : a numpy array containing the features
    - y : a vector containing the target

    Returns
    -------
    """
    print(metrics_dict)

    # Split in folds
    kf = KFold(n_splits=Config.KFOLD, shuffle=True, random_state=Config.RANDOM_STATE)

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

        X_train = X[train_index, :]
        X_test = X[test_index, :]
        y_train = y[train_index]
        y_test = y[test_index]

        # Loop on models
        for model_name, model_param in Config.MODEL_LIST:

            # Model class
            model_class = models_dict[model_name]

            # Instanciate model
            model = model_class(**model_param)

            # Fit the model
            model.fit(X_train, y_train)

            # Predict
            y_predict = model.predict(X_test)

            # Add prediction to lists
            fold_id_predict_list += [fold_index]*len(y_test)
            model_name_predict_list += [model_name]*len(y_test)
            y_test_list += y_test.tolist()
            y_predict_list += y_predict.tolist()

            # Parameters y for metrics
            metric_param_y = {
                'y_true' : y_test,
                'y_pred' : y_predict,
            }

            # Loop on metric
            for metric_name, metric_param in Config.METRIC_LIST:
                
                # Metric function
                metric_function = metrics_dict[metric_name]

                # Parameters for metric
                metric_param_extended = {**metric_param_y, **metric_param}
                metric_value = metric_function(**metric_param_extended)

                # Add metric to lists
                fold_id_metric_list.append(fold_index)
                model_name_metric_list.append(model_name)
                metric_name_list.append(metric_name)
                metric_value_list.append(metric_value)


    # Dict for predictions results
    predictions_dict = {'fold_id': fold_id_predict_list, 'model_name': model_name_predict_list, 'y_test': y_test_list, 'y_predict': y_predict_list}
    predictions_df = pd.DataFrame.from_dict(predictions_dict)

    # Dict for metrics results
    metrics_dict = {'fold_id': fold_id_metric_list, 'model_name': model_name_metric_list, 'metric_name': metric_name_list, 'metric_value': metric_value_list}
    metrics_df = pd.DataFrame.from_dict(metrics_dict)

    # To csv
    predictions_df.to_csv(C.ML_PATH / C.PREDICTIONS_SANDBOX_FILENAME)
    metrics_df.to_csv(C.ML_PATH / C.METRICS_SANDBOX_FILENAME)


# Load data
X,y = load_features_target()
crossval(X, y)