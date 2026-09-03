import argparse
import os
import logging
import pickle
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.temporal_trends import plot_trends

def main():
    parser = argparse.ArgumentParser(description="Generate Temporal Trend Charts")
    parser.add_argument("--storms", type=str, default="data/processed/storms.pkl")
    parser.add_argument("--climate", type=str, default="data/processed/climate.pkl")
    parser.add_argument("--output", type=str, default="outputs/figures/temporal_trends.png")
    args = parser.parse_args()

    with open(args.storms, "rb") as f:
        storm_df = pickle.load(f)
    with open(args.climate, "rb") as f:
        clim_df = pickle.load(f)

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    plot_trends(storm_df, clim_df, args.output)

if __name__ == "__main__":
    main()
