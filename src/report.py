import logging

logger = logging.getLogger(__name__)

def print_report(df, tor_df, clim_df, state_df, deaths):
    """Calculates final summary stats and prints them as a formatted report."""
    
    # Economic stats
    tot_dmg = df['TOTAL_USD'].sum() / 1e9
    top_state = state_df['Total_Damage_Billion_2023'].idxmax()
    top_state_val = state_df.loc[top_state, 'Total_Damage_Billion_2023']
    
    # Mortality stats
    top_killer = deaths.idxmax()
    
    # Tornado regional counts
    plains_n = len(tor_df[tor_df['REGION'] == 'Plains (Tornado Alley)'])
    dixie_n = len(tor_df[tor_df['REGION'] == 'Southeast (Dixie Alley)'])

    # Climate baseline shift: compare early 2010s to early 2020s
    t_2010s = clim_df[clim_df['Year'].between(2010, 2015)]['Max_Temp_F'].mean()
    t_2020s = clim_df[clim_df['Year'].between(2020, 2023)]['Max_Temp_F'].mean()

    logger.info("=" * 65)
    logger.info("THE STATE OF US SEVERE WEATHER (2010-2023) - FINAL SYNTHESIS")
    logger.info("=" * 65)
    logger.info("1. ECONOMIC TOLL (Inflation Adjusted to Constant 2023 USD):")
    logger.info(f"   - Cumulative nationwide weather damage: ${tot_dmg:,.2f} Billion.")
    logger.info(f"   - Most impacted state: {top_state} (${top_state_val:,.2f} Billion).")
    logger.info("2. HUMAN MORTALITY:")
    logger.info(f"   - Leading weather killer: {top_killer} ({int(deaths.max()):,} documented fatalities).")
    logger.info("3. TORNADO ALLEY DYNAMICS:")
    logger.info(f"   - Touchdowns — Plains: {plains_n:,} | Southeast (Dixie): {dixie_n:,}.")
    logger.info("   - Longer Southeastern track durations amplify mortality risks in Dixie Alley.")
    logger.info("4. URBAN CLIMATE BASELINE (NYC Central Park Station USW00094728):")
    logger.info(f"   - Mean Max Temp shift from early 2010s to early 2020s: +{t_2020s - t_2010s:.2f}°F.")
    logger.info("=" * 65)
