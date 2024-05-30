from dotenv import load_dotenv
import os
from pathlib import Path

# Load the .env file
load_dotenv()

class Constants:
    # Paths
    DATA_PATH = Path(os.getenv('DATA_PATH'))
    RAW_PATH = DATA_PATH / 'raw'
    ML_PATH = DATA_PATH / 'ml'

    # Filenames
    RAW_FILENAME = 'data_raw.sav'
