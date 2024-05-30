import pandas as pd

from constants import Constants as C

def load_raw_data():
    df = pd.read_spss(C.RAW_PATH / C.RAW_FILENAME)
    breakpoint()

if __name__ == "__main__":
    load_raw_data()
