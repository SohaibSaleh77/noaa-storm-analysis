import argparse
import os
import logging
import pickle
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.spatial_analysis import make_heatmap

def main():
    parser = argparse.ArgumentParser(description="Generate Interactive Folium Tornado Heatmap")
    parser.add_argument("--input", type=str, default="data/processed/storms.pkl")
    parser.add_argument("--output", type=str, default="outputs/maps/tornado_heatmap.html")
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        df = pickle.load(f)

    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        
    make_heatmap(df, args.output)

if __name__ == "__main__":
    main()
