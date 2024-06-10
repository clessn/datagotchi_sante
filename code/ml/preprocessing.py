from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer, KNNImputer, SimpleImputer
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler

# Dictionnary of available scalers
available_scalers_dict = {
    "std": StandardScaler(),
    "minmax": MinMaxScaler(),
    "robust": RobustScaler(),
}

# Dictionnary of available strategies to impute missing values in X
available_imputers_dict = {
    "imputer_mean": SimpleImputer(strategy="mean"),
    "imputer_median": SimpleImputer(strategy="median"),
    "imputer_most_frequent": SimpleImputer(strategy="most_frequent"),
    "imputer_knn": KNNImputer(n_neighbors=5),
    "imputer_iterative": IterativeImputer(max_iter=10, random_state=42),
}
