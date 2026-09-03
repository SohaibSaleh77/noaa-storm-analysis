import os
import logging
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-darkgrid')
logger = logging.getLogger(__name__)

def plot_impact(df, output_dir, top_n=10):
    """Generates horizontal bar charts for top 10 costliest and deadliest event types."""
    logger.info("Generating Socio-Economic Impact Analysis...")
    fig, ax = plt.subplots(1, 2, figsize=(18, 7))
    fig.suptitle('Socio-Economic Impact (2010-2023, Constant 2023 USD)', fontsize=15, fontweight='bold')

    # Aggregate property + crop damage by event type
    dmg = df.groupby('EVENT_TYPE')['TOTAL_USD'].sum().sort_values(ascending=False).head(top_n) / 1e9
    # invert_yaxis() puts the highest value at the top
    dmg.plot(kind='barh', ax=ax[0], color='crimson').invert_yaxis()
    ax[0].set(title=f'Top {top_n} Events by Economic Damage', xlabel='Billions ($ USD)', ylabel='Event Type')

    # Aggregate deaths by event type
    deaths = df.groupby('EVENT_TYPE')['TOTAL_DEATHS'].sum().sort_values(ascending=False).head(top_n)
    deaths.plot(kind='barh', ax=ax[1], color='black').invert_yaxis()
    ax[1].set(title=f'Top {top_n} Events by Human Fatalities', xlabel='Total Direct + Indirect Fatalities', ylabel='Event Type')

    plt.tight_layout()
    out_path = os.path.join(output_dir, 'socioeconomic_impact_overview.png')
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Saved: {out_path}")
    return dmg, deaths

def plot_state_dmg(df, output_dir, top_n=10):
    """Creates a stacked bar chart breaking down Property vs. Crop damage by state."""
    logger.info("Generating Property vs. Crop Damage Segmentation...")
    
    # Group by state and isolate property vs crop
    split = df.groupby('STATE')[['PROP_USD', 'CROP_USD']].sum()
    split['Total'] = split.sum(axis=1)
    
    # Sort by total, take top N, and drop the helper column
    top = split.nlargest(top_n, 'Total').drop(columns='Total') / 1e9

    top.plot(kind='barh', stacked=True, figsize=(10, 6), color=['#2c3e50', '#27ae60'])
    plt.title(f'Property vs. Crop Damage by State (Top {top_n}, Constant 2023 USD)', fontsize=14, fontweight='bold')
    plt.xlabel('Billions ($ USD)')
    plt.ylabel('State')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    
    out_path = os.path.join(output_dir, 'state_damage_split.png')
    plt.savefig(out_path)
    plt.close()
    logger.info(f"Saved: {out_path}")

def calc_vulnerabilities(df, top_n=10):
    """Calculates a vulnerability matrix (events, damage, deaths, severity index) per state."""
    logger.info(f"--- State Vulnerability Matrix (Top {top_n} States by Total Damage) ---")
    
    # Use named aggregations for clarity
    matrix = df.groupby('STATE').agg(
        Total_Events=('EVENT_ID', 'nunique'),
        Total_Damage_Billion_2023=('TOTAL_USD', lambda x: x.sum() / 1e9),
        Total_Deaths=('TOTAL_DEATHS', 'sum')
    ).sort_values(by='Total_Damage_Billion_2023', ascending=False).head(top_n)

    # Calculate a derived metric: Damage per event in Millions
    matrix['Severity_Index_DamagePerEvent_M'] = (matrix['Total_Damage_Billion_2023'] * 1000) / matrix['Total_Events']
    
    # Log the dataframe as a string for console visibility
    logger.info(f"\n{matrix.round(2).to_string()}")
    return matrix

def run_impact_analysis(df, output_dir):
    """Master function for Socio-Economic analysis."""
    dmg, deaths = plot_impact(df, output_dir)
    plot_state_dmg(df, output_dir)
    state_df = calc_vulnerabilities(df)
    return dmg, deaths, state_df
