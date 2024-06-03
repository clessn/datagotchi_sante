from sklearn.model_selection import KFold

from config import Config as Config

def crossval (X, Y):
    """ Cross-validation (evaluation realized for each fold of each model)

    Attributes
    ----------
    - X : a numpy array containing the features
    - Y : a numpy array containing the targets

    Returns
    -------
    """

    # Loop on models
    for model in Config.MODEL_LIST:

        # Split in folds
        kf = KFold(n_splits=Config.KFOLD, shuffle=True, random_state=Config.RANDOM_STATE)

        # Loop on folds
        for train_index, test_index in kf.split(X):

            # Loop on target
            for target in Config.TARGET_LIST:

                # Loop on metric
                for metrics in Config.METRIC_LIST:

