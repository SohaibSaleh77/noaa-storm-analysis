#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "Step 1: Fetching Storm Data..."
python scripts/fetch_storms.py --start 2010 --end 2023 --output data/processed/storms.pkl

echo "Step 2: Fetching Climate Data..."
python scripts/fetch_climate.py --station "GHCND:USW00094728" --start 2010 --end 2023 --output data/processed/climate.pkl

echo "Step 3: Plotting Trends..."
python scripts/plot_trends.py --storms data/processed/storms.pkl --climate data/processed/climate.pkl --output outputs/figures/temporal_trends.png

echo "Step 4: Plotting Maps..."
python scripts/plot_maps.py --input data/processed/storms.pkl --output outputs/figures/spatial_distribution_scatter.png

echo "Step 5: Plotting Heatmap..."
python scripts/plot_heatmap.py --input data/processed/storms.pkl --output outputs/maps/tornado_heatmap.html

echo "Step 6: Analyzing Tornadoes..."
python scripts/analyze_tornadoes.py --input data/processed/storms.pkl --output_dir outputs/figures

echo "Step 7: Analyzing Impact..."
python scripts/analyze_impact.py --input data/processed/storms.pkl --output_dir outputs/figures

echo "Step 8: Generating Final Report..."
python scripts/generate_report.py --storms data/processed/storms.pkl --climate data/processed/climate.pkl

echo "Pipeline completed successfully!"
