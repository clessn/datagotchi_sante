import numpy as np
from config import Config
from sklearn.metrics import mean_squared_error

import logging
logger = logging.getLogger(__name__)

# Remove missing values from y vectors
def remove_y_true_nan(y_true, y_pred):
    true_nan_indices = np.isnan(y_true)

    # Assert minimal number of targets
    assert sum(~true_nan_indices) >= Config.MIN_TEST_SIZE

    # Filter y vectors
    y_true_filtered = y_true[~true_nan_indices]
    y_pred_filtered = y_pred[~true_nan_indices]

    return y_true_filtered, y_pred_filtered


# MSE
def get_mse(y_true, y_pred):

    # Remove missing values
    y_true_filtered, y_pred_filtered = remove_y_true_nan(y_true, y_pred)

    # Metric
    mse = mean_squared_error(y_true_filtered, y_pred_filtered)
    logger.error('mse computed')
    return mse


# Dictionnary of available metrics
available_metrics_dict = {
    "mse": (get_mse, {}),
}
