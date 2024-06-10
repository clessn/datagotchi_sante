
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Dictionnary of available scalers
available_scalers_dict = {
    "std": StandardScaler(),
    "minmax": MinMaxScaler(),
    "robust": RobustScaler(),
}

# Dictionnary of available strategies to impute missing values in X
available_imputers_dict = {
    "imputer_mean": SimpleImputer(strategy="mean"),
}
