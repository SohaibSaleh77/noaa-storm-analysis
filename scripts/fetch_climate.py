import argparse
import os
import logging
import pickle
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.climate_data import get_climate

def main():
    parser = argparse.ArgumentParser(description="Fetch NOAA Climate Data")
    parser.add_argument("--station", type=str, default="GHCND:USW00094728")
    parser.add_argument("--start", type=int, default=2010)
    parser.add_argument("--end", type=int, default=2023)
    parser.add_argument("--output", type=str, default="data/processed/climate.pkl")
    args = parser.parse_args()

    df = get_climate(station=args.station, start=args.start, end=args.end)
    
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    with open(args.output, "wb") as f:
        pickle.dump(df, f)
    logging.info(f"Saved climate data to {args.output}")

if __name__ == "__main__":
    main()
