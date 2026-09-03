import time
import logging
import pandas as pd
from src.utils import get_url, parse_dmg
from src.config import CPI_TO_2023

logger = logging.getLogger(__name__)

def fetch_year(yr):
    """Downloads a single year of storm data and loads it into a DataFrame."""
    url = get_url(yr)
    try:
        # Read directly from the gzip CSV stream
        df = pd.read_csv(url, compression='gzip', low_memory=False)
        logger.info(f"Downloaded {yr} successfully. ({len(df):,} records)")
        
        # Brief pause to be polite to the NOAA server and avoid rate limits
        time.sleep(0.3)
        return df
    except Exception as e:
        raise RuntimeError(f"Fatal Error: Failed to download/parse {yr}.") from e

def clean_storms(raw_df):
    """
    Filters columns, parses dates, extracts damage values, and adjusts for inflation.
    """
    # Define the exact columns needed for downstream analysis to keep memory footprint low
    cols = [
        'BEGIN_YEARMONTH', 'BEGIN_DATE_TIME', 'END_DATE_TIME', 'EPISODE_ID', 'EVENT_ID',
        'STATE', 'STATE_FIPS', 'CZ_NAME', 'EVENT_TYPE', 'BEGIN_LAT', 'BEGIN_LON',
        'END_LAT', 'END_LON', 'INJURIES_DIRECT', 'INJURIES_INDIRECT', 'DEATHS_DIRECT',
        'DEATHS_INDIRECT', 'DAMAGE_PROPERTY', 'DAMAGE_CROPS'
    ]
    
    # Use a list comprehension to avoid KeyErrors if a column is missing in an older year
    df = raw_df[[c for c in cols if c in raw_df.columns]].copy()
    
    # Parse the custom date format used by NOAA (e.g., '01-JAN-10 12:00:00')
    df['BEGIN_DATE_TIME'] = pd.to_datetime(df['BEGIN_DATE_TIME'], format='%d-%b-%y %H:%M:%S', errors='coerce')
    df['END_DATE_TIME'] = pd.to_datetime(df['END_DATE_TIME'], format='%d-%b-%y %H:%M:%S', errors='coerce')
    df['YEAR'] = df['BEGIN_DATE_TIME'].dt.year
    df['MONTH'] = df['BEGIN_DATE_TIME'].dt.month

    # Financial parsing: convert string shorthand to raw USD floats
    df['PROP_USD_RAW'] = parse_dmg(df['DAMAGE_PROPERTY'])
    df['CROP_USD_RAW'] = parse_dmg(df['DAMAGE_CROPS'])

    # Inflation normalization to 2023 dollars using CPI map.
    # If a year isn't in our CPI map, fillna(1.0) assumes no adjustment needed.
    cpi_mult = df['YEAR'].map(CPI_TO_2023).fillna(1.0)
    df['PROP_USD'] = df['PROP_USD_RAW'] * cpi_mult
    df['CROP_USD'] = df['CROP_USD_RAW'] * cpi_mult
    df['TOTAL_USD'] = df['PROP_USD'] + df['CROP_USD']
    
    # Sum direct and indirect deaths for a holistic mortality metric
    df['TOTAL_DEATHS'] = df['DEATHS_DIRECT'] + df['DEATHS_INDIRECT']
    return df

def get_storms(start=2010, end=2023):
    """Main function to loop through years, fetch, and clean storm data."""
    logger.info("--- Fetching NOAA Storm Events Data ---")
    dfs = [fetch_year(yr) for yr in range(start, end + 1)]
    if not dfs:
        raise RuntimeError("Fatal Error: No storm data retrieved.")
        
    # Combine all years into a single DataFrame
    clean_df = clean_storms(pd.concat(dfs, ignore_index=True))
    logger.info(f"Storm Data Ready. Total Records: {len(clean_df):,} | Shape: {clean_df.shape}")
    return clean_df
