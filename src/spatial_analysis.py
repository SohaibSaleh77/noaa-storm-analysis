import logging
import matplotlib.pyplot as plt
import folium
from folium.plugins import HeatMap

plt.style.use('seaborn-v0_8-darkgrid')
logger = logging.getLogger(__name__)

def filter_spatial(df, ev_types=['Tornado', 'Hail']):
    """
    Filters events to only include valid lat/lon points within the US bounds.
    Some NOAA records have missing or zero coordinates which break maps.
    """
    sub = df[df['EVENT_TYPE'].isin(ev_types)].dropna(subset=['BEGIN_LAT', 'BEGIN_LON']).copy()
    
    # Apply bounding box for continental US to filter out bad data points
    return sub[(sub['BEGIN_LAT'] > 20) & (sub['BEGIN_LON'] < -60) & (sub['BEGIN_LON'] > -130)]

def plot_maps(df, output_path):
    """Creates side-by-side static scatter maps for Tornadoes and Hail."""
    logger.info("Generating Spatial Scatter Maps...")
    spat = filter_spatial(df)
    fig, ax = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('Spatial Distribution of Severe Events (2010-2023)', fontsize=15, fontweight='bold')

    # Tornado Scatter
    tor = spat[spat['EVENT_TYPE'] == 'Tornado']
    ax[0].scatter(tor['BEGIN_LON'], tor['BEGIN_LAT'], c='red', alpha=0.25, s=8, edgecolors='none')
    ax[0].set(title=f'Tornado Touchdowns (n={len(tor):,})', xlabel='Longitude', ylabel='Latitude', xlim=(-125, -65), ylim=(25, 50))

    # Hail Scatter
    hail = spat[spat['EVENT_TYPE'] == 'Hail']
    ax[1].scatter(hail['BEGIN_LON'], hail['BEGIN_LAT'], c='green', alpha=0.1, s=8, edgecolors='none')
    ax[1].set(title=f'Severe Hail Reports (n={len(hail):,})', xlabel='Longitude', ylabel='Latitude', xlim=(-125, -65), ylim=(25, 50))

    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Saved: {output_path}")
    plt.close()

def make_heatmap(df, output_path):
    """Generates an interactive Folium heatmap HTML file for Tornadoes."""
    logger.info("Generating Full-Density Interactive Tornado Heatmap...")
    tor = filter_spatial(df, ['Tornado'])
    
    # Center map on the US
    m = folium.Map(location=[39.5, -98.35], zoom_start=4, tiles='CartoDB dark_matter')
    if not tor.empty:
        # Extract coordinates as list of lists for Folium
        heat_data = tor[['BEGIN_LAT', 'BEGIN_LON']].values.tolist()
        HeatMap(heat_data, radius=9, blur=14, max_zoom=10).add_to(m)
    m.save(output_path)
    logger.info(f"Saved: {output_path}")
