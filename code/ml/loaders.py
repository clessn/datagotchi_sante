import pandas as pd
from constants import Constants as C


def explore_raw_data():
    df_str = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME, convert_categoricals=True)
    df_num = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME, convert_categoricals=False)
    df_num.to_csv('attributes.csv')
    return df_str, df_num

def load_codebook():
    df = pd.read_csv(C.ML_PATH / C.CODEBOOK_FILENAME)
    return df

if __name__ == "__main__":
    df_str, df_num = explore_raw_data()
    print(df_str.info(verbose=True))
    breakpoint()
