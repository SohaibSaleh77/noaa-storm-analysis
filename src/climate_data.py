import time
import logging
import requests
import pandas as pd
from src.config import CDO_TOKEN

logger = logging.getLogger(__name__)

def fetch_ghcn(station, start, end, token):
    """
    Paginates through the CDO API to pull daily GHCN data for a given station.
    The API limits us to 1000 records per call, so we use 'offset' to get all days in a year.
    """
    logger.info("--- Fetching Daily Climate Data (GHCN) via CDO API ---")
    headers = {'token': token}
    records = []
    
    for yr in range(start, end + 1):
        offset = 1
        while True:
            params = {
                'datasetid': 'GHCND', 
                'stationid': station,
                'startdate': f"{yr}-01-01", 
                'enddate': f"{yr}-12-31",
                'datatypeid': ['TMAX', 'PRCP'],  # Max Temp & Precipitation
                'limit': 1000,                   # API max limit
                'units': 'standard',             # Fahrenheit and Inches
                'offset': offset
            }
            res = requests.get('https://www.ncei.noaa.gov/cdo-web/api/v2/data', headers=headers, params=params, timeout=30)
            
            if res.status_code == 200:
                data = res.json().get('results', [])
                if not data: 
                    # Empty data means we've exhausted records for this year
                    break
                    
                records.extend(data)
                offset += 1000
                time.sleep(0.3)  # Be polite to API
            elif res.status_code == 429:
                # Handle rate limiting by pausing longer
                logger.warning(f"Rate limit hit on {yr}. Pausing 5s...")
                time.sleep(5)
            else:
                raise RuntimeError(f"Fatal Error: CDO API failed for {yr}. Status: {res.status_code}")
        logger.info(f"Fetched climate data for {yr}")
    return records

def get_climate(station="GHCND:USW00094728", start=2010, end=2023, token=CDO_TOKEN):
    """Converts raw API JSON into a structured Pandas DataFrame."""
    records = fetch_ghcn(station, start, end, token)
    
    # The API returns data in a long format (one row per datatype per day).
    # We pivot it so TMAX and PRCP become columns, making it easier to analyze.
    df = pd.DataFrame(records).pivot_table(index='date', columns='datatype', values='value').reset_index()
    
    df['date'] = pd.to_datetime(df['date'])
    df.rename(columns={'TMAX': 'Max_Temp_F', 'PRCP': 'Precip_In'}, inplace=True)
    df['Year'] = df['date'].dt.year
    logger.info(f"Climate Data Ready (Station {station}). Shape: {df.shape}")
    return df
