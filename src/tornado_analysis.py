import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

plt.style.use('seaborn-v0_8-darkgrid')
logger = logging.getLogger(__name__)

def get_region(state):
    """Categorizes states into Plains (Tornado Alley) or Southeast (Dixie Alley)."""
    plains = {'TEXAS', 'OKLAHOMA', 'KANSAS', 'NEBRASKA', 'SOUTH DAKOTA', 'NORTH DAKOTA'}
    se = {'MISSISSIPPI', 'ALABAMA', 'GEORGIA', 'TENNESSEE', 'ARKANSAS', 'LOUISIANA'}
    return 'Plains (Tornado Alley)' if state in plains else ('Southeast (Dixie Alley)' if state in se else 'Other')

def prep_tornadoes(df):
    """Extracts tornadoes, calculates hour of day, region, and path duration in minutes."""
    tor = df[df['EVENT_TYPE'] == 'Tornado'].copy()
    tor['HOUR'] = tor['BEGIN_DATE_TIME'].dt.hour
    tor['REGION'] = tor['STATE'].apply(get_region)
    
    # Calculate duration on ground in minutes
    tor['DURATION_MINS'] = (tor['END_DATE_TIME'] - tor['BEGIN_DATE_TIME']).dt.total_seconds() / 60
    return tor

def plot_diurnal(df, output_path):
    """Plots histogram of touchdowns by hour and seasonal line plot by region."""
    logger.info("Generating Tornado Diurnal & Seasonality Analysis...")
    fig, ax = plt.subplots(1, 2, figsize=(16, 6))
    fig.suptitle('Anatomy of Tornadoes (2010-2023)', fontsize=15, fontweight='bold')

    # Histogram of hours
    sns.histplot(df['HOUR'], bins=24, kde=False, ax=ax[0], color='purple')
    ax[0].set(title='Diurnal Distribution of Tornado Touchdowns', xlabel='Hour of Day (0-23)', ylabel='Count')
    ax[0].set_xticks(range(0, 24, 2))

    # Seasonality line plot
    sub = df[df['REGION'] != 'Other']
    season = sub.groupby(['MONTH', 'REGION']).size().unstack().fillna(0)
    season.plot(kind='line', ax=ax[1], marker='o')
    ax[1].set(title='Seasonality: Plains vs. Southeast', xlabel='Month', ylabel='Count')
    ax[1].set_xticks(range(1, 13))

    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Saved: {output_path}")
    plt.close()

def plot_tor_grid(df, output_path):
    """Creates a 2D heatmap showing Tornado frequency by Hour and Month."""
    logger.info("Generating 2D Temporal Heatmap for Tornadoes...")
    plt.figure(figsize=(11, 7))
    
    # Pivot table: rows=Hours, cols=Months, values=count of EVENT_IDs
    grid = df.pivot_table(index='HOUR', columns='MONTH', values='EVENT_ID', aggfunc='count').fillna(0)
    sns.heatmap(grid, cmap='magma', linewidths=.5)
    
    plt.title('Tornado Frequency: Hour of Day vs. Month of Year', fontsize=14, fontweight='bold')
    plt.xlabel('Month (1=Jan, 12=Dec)')
    plt.ylabel('Hour of Day (0-23)')
    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Saved: {output_path}")
    plt.close()

def plot_duration(df, output_path):
    """Creates a boxplot comparing Tornado track durations between Plains and Southeast."""
    logger.info("Generating Tornado Duration Analysis...")
    
    # Filter out negative durations (data errors)
    valid = df[df['DURATION_MINS'] >= 0].copy()
    sub = valid[valid['REGION'] != 'Other']

    plt.figure(figsize=(8, 6))
    # showfliers=False hides extreme outliers so the box quartiles are visible
    sns.boxplot(data=sub, x='REGION', y='DURATION_MINS', showfliers=False, palette='Set2')
    plt.title('Tornado Track Duration: Plains vs. Southeast', fontsize=14, fontweight='bold')
    plt.ylabel('Duration on Ground (Minutes)')
    plt.xlabel('Region')
    plt.tight_layout()
    plt.savefig(output_path)
    logger.info(f"Saved: {output_path}")
    plt.close()
    return valid

def print_tor_stats(df, dur_df):
    """Performs non-parametric Mann-Whitney U test to compare regional durations."""
    plains = dur_df[dur_df['REGION'] == 'Plains (Tornado Alley)']['DURATION_MINS'].dropna()
    dixie = dur_df[dur_df['REGION'] == 'Southeast (Dixie Alley)']['DURATION_MINS'].dropna()

    # alternative='greater' tests if Dixie durations are stochastically greater than Plains
    stat, p_val = stats.mannwhitneyu(dixie, plains, alternative='greater')

    logger.info("--- Tornado Statistical Insights ---")
    logger.info(f"1. Peak Tornado Hour: {int(df['HOUR'].mode()[0])}:00 local time.")
    logger.info(f"2. Median Track Duration — Plains: {plains.median():.1f} min | Southeast: {dixie.median():.1f} min.")
    logger.info(f"3. Statistical Significance Test (Mann-Whitney U): p-value = {p_val:.4e}.")
    if p_val < 0.01:
        logger.info("   -> CONCLUSION: Statistically significant proof (p < 0.01) that Southeast tornadoes remain on the ground longer.")
    else:
        logger.info("   -> CONCLUSION: No statistically significant difference in duration detected.")

def run_tornado_analysis(df, output_dir):
    """Master function for Tornado analysis. Generates plots and runs stats."""
    tor_df = prep_tornadoes(df)
    plot_diurnal(tor_df, os.path.join(output_dir, 'tornado_diurnal_seasonal.png'))
    plot_tor_grid(tor_df, os.path.join(output_dir, 'tornado_hour_month_grid.png'))
    valid_dur = plot_duration(tor_df, os.path.join(output_dir, 'tornado_duration_boxplot.png'))
    print_tor_stats(tor_df, valid_dur)
    return tor_df
