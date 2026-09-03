import re
import logging
import requests
import pandas as pd
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def get_url(yr):
    """
    Scrapes the NOAA directory to find the exact CSV.gz URL for a given year.
    NOAA updates these files periodically, appending a timestamp to the filename.
    This ensures we always grab the latest version for the requested year.
    """
    base = "https://www.ncei.noaa.gov/pub/data/swdi/stormevents/csvfiles/"
    res = requests.get(base, timeout=30)
    res.raise_for_status()
    
    # Parse the HTML directory listing
    soup = BeautifulSoup(res.text, 'html.parser')
    
    # Look for the pattern matching the requested year
    pat = f"StormEvents_details-ftp_v1.0_d{yr}_c"
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith(pat) and href.endswith('.csv.gz'):
            return base + href
            
    raise RuntimeError(f"Fatal Error: Could not locate CSV for {yr} on NOAA server.")

def parse_dmg(series):
    """
    Vectorized string parsing for damage values.
    NOAA storm data stores damages as strings like '10.5K' or '2.00M'.
    We extract the numeric portion and multiply by the appropriate magnitude.
    """
    s = series.astype(str).str.upper().str.strip()
    
    # Extract the numeric part using regex. If it fails, default to 0.0
    num = s.str.extract(r'([\d\.]+)')[0].astype(float).fillna(0.0)
    
    # Default multiplier is 1.0 (for exact dollars)
    mult = pd.Series(1.0, index=s.index)
    
    # Apply multipliers based on suffix letters
    mult.loc[s.str.contains('K', na=False)] = 1e3  # Thousand
    mult.loc[s.str.contains('M', na=False)] = 1e6  # Million
    mult.loc[s.str.contains('B', na=False)] = 1e9  # Billion
    
    return num * mult
