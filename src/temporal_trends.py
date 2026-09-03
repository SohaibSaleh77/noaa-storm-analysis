import logging
import matplotlib.pyplot as plt
import seaborn as sns

plt.style.use('seaborn-v0_8-darkgrid')
logger = logging.getLogger(__name__)

def calc_freq(df, top_n=5):
    """Counts occurrences of the top 5 most frequent storm types per year."""
    # Find the top N events overall
    top = df['EVENT_TYPE'].value_counts().nlargest(top_n).index
    # Filter to only those events, group by Year and Type, then unstack for plotting
    return df[df['EVENT_TYPE'].isin(top)].groupby(['YEAR', 'EVENT_TYPE']).size().unstack().fillna(0), top

def calc_dmg(df):
    """Sums total economic damage per year in billions."""
    return df.groupby('YEAR')['TOTAL_USD'].sum() / 1e9

def calc_heat(df, thresh=90):
    """Counts days where max temp exceeded threshold (e.g., 90°F)."""
    return df[df['Max_Temp_F'] > thresh].groupby('Year').size()

def calc_precip(df):
    """Finds the maximum 1-day precipitation for each year."""
    return df.groupby('Year')['Precip_In'].max()

def plot_trends(storm_df, clim_df, output_path):
    """Builds a 2x2 grid of line/bar charts showing trends."""
    logger.info("Generating Temporal Trend Charts...")
    freq, top_ev = calc_freq(storm_df)
    dmg = calc_dmg(storm_df)
    heat = calc_heat(clim_df)
    precip = calc_precip(clim_df)

    fig, ax = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle('Temporal Trends in Severe Weather & Climate (2010-2023, Inflation Adjusted)', fontsize=15, fontweight='bold')

    # Top Left: Event Frequency Line Plot
    freq.plot(ax=ax[0, 0], marker='o')
    ax[0, 0].set(title='Annual Frequency of Top 5 Severe Events', ylabel='Event Count', xlabel='Year')
    ax[0, 0].legend(title='Event Type', bbox_to_anchor=(1.02, 1), loc='upper left')

    # Top Right: Economic Damage Bar Chart
    dmg.plot(kind='bar', ax=ax[0, 1], color='darkred')
    ax[0, 1].set(title='Annual Total Economic Damage (Billions, Constant 2023 USD)', ylabel='Billions ($ USD)', xlabel='Year')

    # Bottom Left: Extreme Heat Days Bar Chart
    heat.plot(kind='bar', ax=ax[1, 0], color='orange')
    ax[1, 0].set(title='Annual Extreme Heat Days (>90°F) - NYC Central Park Baseline', ylabel='Days', xlabel='Year')

    # Bottom Right: Max Precipitation Line Plot
    precip.plot(ax=ax[1, 1], marker='s', color='blue')
    ax[1, 1].set(title='Annual Max 1-Day Precipitation (Inches)', ylabel='Inches', xlabel='Year')

    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Saved: {output_path}")
    plt.close()
