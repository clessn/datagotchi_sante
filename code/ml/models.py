import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.tree import ExtraTreeRegressor

from config import Config
from preprocessing import available_imputers_dict
from preprocessing import available_scalers_dict


class MeanRegressor(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.mean_ = None

    def fit(self, X, y):
        """
        Fit the model by calculating the mean of the target values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target values

        Returns
        -------
        self : object
            Returns self.
        """
        self.mean_ = np.nanmean(y)
        return self

    def predict(self, X):
        """
        Predict the mean target value for all samples in X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Samples

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Predicted mean target values
        """
        return np.full(shape=(X.shape[0],), fill_value=self.mean_)


class RandomValueRegressor(BaseEstimator, RegressorMixin):
    def __init__(self):
        self.min_ = None
        self.max_ = None

    def fit(self, X, y):
        """
        Fit the model by calculating the min and max of the target values.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Training data
        y : array-like, shape (n_samples,)
            Target values

        Returns
        -------
        self : object
            Returns self.
        """
        self.min_ = np.nanmin(y)
        self.max_ = np.nanmax(y)
        return self

    def predict(self, X):
        """
        Predict a random value between the min and max target values for each sample in X.

        Parameters
        ----------
        X : array-like, shape (n_samples, n_features)
            Samples

        Returns
        -------
        y_pred : array, shape (n_samples,)
            Predicted random values
        """
        return np.random.uniform(low=self.min_, high=self.max_, size=X.shape[0])


# Dictionnary of available models
available_models_dict = {
    "mean_regressor": MeanRegressor(),
    "random_regressor": RandomValueRegressor(),
    "extra_tree_regressor": Pipeline(
        [
            (Config.SCALER_CHOICE["extra_tree_regressor"], available_scalers_dict[Config.SCALER_CHOICE["extra_tree_regressor"]]),
            (Config.IMPUTER_CHOICE["extra_tree_regressor"], available_imputers_dict[Config.IMPUTER_CHOICE["extra_tree_regressor"]]),
            ("regressor", ExtraTreeRegressor(random_state=42)),
        ]
    ),
    "linear_regressor": Pipeline(
        [
            (Config.SCALER_CHOICE["linear_regressor"], available_scalers_dict[Config.SCALER_CHOICE["linear_regressor"]]),
            (Config.IMPUTER_CHOICE["linear_regressor"], available_imputers_dict[Config.IMPUTER_CHOICE["linear_regressor"]]),
            ("regressor", LinearRegression()),
        ]
    ),
}
