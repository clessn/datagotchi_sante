from sklearn.model_selection import KFold
import pandas as pd

from constants import Constants as C
from config import Config as Config
from loaders import load_features_target


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
    kf = KFold(n_splits=Config.KFOLD, shuffle=True, random_state=Config.RANDOM_STATE)

    # Lists for results
    fold_id_list = []
    model_name_list = []
    y_test_list = []
    y_predict_list = []


    # Loop on folds
    for fold_index, (train_index, test_index) in enumerate(kf.split(X)):

        X_train = X[train_index, :]
        X_test = X[test_index, :]
        y_train = y[train_index]
        y_test = y[test_index]

        # Loop on models
        for model_class, model_name, model_param in Config.MODEL_LIST:

            # Instanciate model
            model = model_class(**model_param)

            # Fit the model
            model.fit(X_train, y_train)

            # Predict
            y_predict = model.predict(X_test)

            # Add prediction to lists
            fold_id_list += [fold_index]*len(y_test)
            model_name_list += [model_name]*len(y_test)
            y_test_list += y_test.tolist()
            y_predict_list += y_predict.tolist()

            # Loop on metric
            for metrics in Config.METRIC_LIST:
                pass

    # Dict for results
    predictions_dict = {'fold_id': fold_id_list, 'model_name': model_name_list, 'y_test': y_test_list, 'y_predict': y_predict_list}
    predictions_df = pd.DataFrame.from_dict(predictions_dict)

    # To csv
    predictions_df.to_csv(C.ML_PATH / C.PREDICTIONS_SANDBOX_FILENAME)


# Load data
X,y = load_features_target()
crossval(X, y)