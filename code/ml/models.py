from sklearn.base import BaseEstimator
from sklearn.base import RegressorMixin
import numpy as np


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
        self.mean_ = np.mean(y)
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
        self.min_ = np.min(y)
        self.max_ = np.max(y)
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