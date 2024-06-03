from config import Config as Config
from sklearn.model_selection import KFold


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

    # Loop on folds
    for train_index, test_index in kf.split(X):

        X_train = X[train_index, :]
        X_test = X[test_index, :]
        y_train = y[train_index]
        y_test = y[test_index]

        # Loop on models
        for model in Config.MODEL_LIST:

            # Fit the model
            model.fit(X_train, y_train)

            # Loop on metric
            for metrics in Config.METRIC_LIST:
                pass
