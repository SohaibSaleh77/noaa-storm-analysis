import argparse
import os
import logging
import pickle
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tornado_analysis import run_tornado_analysis

def main():
    parser = argparse.ArgumentParser(description="Run Tornado Analysis")
    parser.add_argument("--input", type=str, default="data/processed/storms.pkl")
    parser.add_argument("--output_dir", type=str, default="outputs/figures")
    args = parser.parse_args()

    with open(args.input, "rb") as f:
        df = pickle.load(f)

    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
        
    run_tornado_analysis(df, args.output_dir)

if __name__ == "__main__":
    main()
