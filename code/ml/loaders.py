import pandas as pd
from constants import Constants as C


def explore_raw_data():
    df_str = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME, convert_categoricals=True)
    df_num = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME, convert_categoricals=False)
    return df_str, df_num


def load_codebook():
    df = pd.read_csv(C.ML_PATH / C.CODEBOOK_FILENAME)
    return df.loc[:, C.CODEBOOK_COLS].drop_duplicates()


def load_attributes():
    df = pd.read_csv(C.ML_PATH / C.ATTRIBUTES_FILENAME)
    df = df.set_index(C.ATTRIBUTE_ID_COL)
    return df


if __name__ == "__main__":
    df_str, df_num = explore_raw_data()
    df_codebook = load_codebook()
    # print(df_str.info(verbose=True))
    df_attributes = load_attributes()
    print(df_attributes.info(verbose=True))
    breakpoint()
