from dotenv import load_dotenv
import os
from pathlib import Path

# Load the .env file
load_dotenv()

class Constants:
    DATA_PATH = Path(os.getenv('PATH'))
    RAW_PATH = DATA_PATH / 'raw'
    ML_PATH = DATA_PATH / 'ml'

