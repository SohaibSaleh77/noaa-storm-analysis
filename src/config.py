import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# BLS Consumer Price Index (CPI) multipliers to normalize all damages to 2023 Dollars.
# We map each year to a multiplier. If a year is missing, we default to 1.0 later.
CPI_TO_2023 = {
    2010: 1.39, 2011: 1.35, 2012: 1.32, 2013: 1.30, 2014: 1.28,
    2015: 1.28, 2016: 1.26, 2017: 1.24, 2018: 1.21, 2019: 1.19,
    2020: 1.17, 2021: 1.12, 2022: 1.04, 2023: 1.00
}

# Securely fetch the API token from environment variables
CDO_TOKEN = os.getenv("CDO_TOKEN", "default_token_if_missing")

# Define base directories relative to this file's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROC = os.path.join(BASE_DIR, 'data', 'processed')
OUT_FIGS = os.path.join(BASE_DIR, 'outputs', 'figures')
OUT_MAPS = os.path.join(BASE_DIR, 'outputs', 'maps')

# Ensure directories exist when this module is imported
for d in [DATA_RAW, DATA_PROC, OUT_FIGS, OUT_MAPS]:
    os.makedirs(d, exist_ok=True)
