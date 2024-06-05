import numpy as np
import pandas as pd
from constants import Constants as C
from loaders import load_attributes, load_codebook

# def create_attribute_sandbox(df_codebook, df_attributes):
#     df_codebook_sandbox = df_codebook.iloc[0:41]
#     available_variables = np.unique(df_codebook_sandbox[C.CODEBOOK_NAME_COL]).tolist()
#     sandbox_variables = available_variables + C.TARGET_COLS
#     df_attributes_sandbox = df_attributes.loc[:, sandbox_variables]
#     df_attributes_sandbox.to_csv(C.ML_PATH / C.ATTRIBUTES_SANDBOX_FILENAME)


# def get_attributes_sandbox():
#     return pd.read_csv(
#         C.ML_PATH / C.ATTRIBUTES_SANDBOX_FILENAME, index_col=C.ATTRIBUTE_ID_COL
#     )


def create_numerical_features(df_attributes):
    numerical_fields = [
        C.CODEBOOK_TYPE_INTEGER_LABEL,
        C.CODEBOOK_TYPE_FLOAT_LABEL,
        C.CODEBOOK_TYPE_ORDINAL_LABEL,
    ]
    numerical_variables = df_codebook.loc[
        df_codebook[C.CODEBOOK_TYPE_COL].isin(numerical_fields), C.CODEBOOK_NAME_COL
    ].values
    print(numerical_variables)
    return df_attributes.loc[:, numerical_variables]


df_codebook = load_codebook()
df_attributes = load_attributes()
# create_attribute_sandbox(df_codebook, df_attributes)
# df_attributes_sandbox = get_attributes_sandbox()
df_numerical_features = create_numerical_features(df_attributes)
df_features = df_numerical_features  # aggregate here different type of features
df_targets = df_attributes.loc[:, C.TARGET_COLS]
df_features.to_csv(C.ML_PATH / C.FEATURES_FILENAME)
df_targets.to_csv(C.ML_PATH / C.TARGETS_FILENAME)
print("Features and Targets created with success !! :-)")
