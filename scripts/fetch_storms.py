import argparse
import os
import logging
import pickle
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.storm_data import get_storms

def main():
    parser = argparse.ArgumentParser(description="Fetch NOAA Storm Data")
    parser.add_argument("--start", type=int, default=2010)
    parser.add_argument("--end", type=int, default=2023)
    parser.add_argument("--output", type=str, default="data/processed/storms.pkl")
    args = parser.parse_args()

    df = get_storms(start=args.start, end=args.end)
    
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    with open(args.output, "wb") as f:
        pickle.dump(df, f)
    logging.info(f"Saved storm data to {args.output}")

if __name__ == "__main__":
    main()
