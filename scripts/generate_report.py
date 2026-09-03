import argparse
import os
import logging
import pickle
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.tornado_analysis import prep_tornadoes
from src.impact_analysis import calc_vulnerabilities
from src.report import print_report

def main():
    parser = argparse.ArgumentParser(description="Generate Final Synthesis Report")
    parser.add_argument("--storms", type=str, default="data/processed/storms.pkl")
    parser.add_argument("--climate", type=str, default="data/processed/climate.pkl")
    args = parser.parse_args()

    with open(args.storms, "rb") as f:
        storm_df = pickle.load(f)
    with open(args.climate, "rb") as f:
        clim_df = pickle.load(f)

    # Recalculate specific minor dataframes needed for the text report
    tor_df = prep_tornadoes(storm_df)
    deaths = storm_df.groupby('EVENT_TYPE')['TOTAL_DEATHS'].sum().sort_values(ascending=False).head(10)
    state_df = calc_vulnerabilities(storm_df)

    print_report(storm_df, tor_df, clim_df, state_df, deaths)

if __name__ == "__main__":
    main()
