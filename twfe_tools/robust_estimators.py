import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.formula.api as smf

def run_robust_comparison(df, y, d, unit, time):
    """
    Standard TWFE estimation using PanelOLS with fixed effects.
    """
    df_panel = df.set_index([unit, time])
    model = PanelOLS.from_formula(f"Q('{y}') ~ Q('{d}') + EntityEffects + TimeEffects", data=df_panel)
    res = model.fit(cov_type='clustered', cluster_entity=True)
    
    print("\n" + "="*30)
    print("      STANDARD TWFE REPORT      ")
    print("="*30)
    # Using .iloc[0] to avoid FutureWarnings
    print(f"TWFE Coefficient: {res.params.iloc[0]:.4f}")
    print(f"Std. Error     : {res.std_errors.iloc[0]:.4f}")
    print(f"P-value        : {res.pvalues.iloc[0]:.4f}")
    print("-"*30)
    
    return res

def run_csdid_simple(df, y, d, unit, time):
    """
    Simplified Callaway & Sant'Anna approach.
    Calculates the Average Treatment Effect on the Treated (ATT) 
    by cohort (group-time) using only clean controls.
    """
    # 1. Identify the 'cohort' (first year of treatment)
    df = df.copy()
    df['first_treat'] = df.groupby(unit)[time].transform(lambda x: x[df[d] == 1].min())
    
    # 2. Define 'Never Treated' as the clean control group
    never_treated = df[df['first_treat'].isna()]
    
    # 3. Calculate ATT for each cohort at each year after treatment
    results = []
    cohorts = df['first_treat'].dropna().unique()
    
    for c in cohorts:
        # Get data for this specific cohort and the clean controls
        cohort_data = df[df['first_treat'] == c]
        comparison_df = pd.concat([cohort_data, never_treated])
        
        # Calculate the simple DiD for this cohort: (Y_post - Y_pre)_treated - (Y_post - Y_pre)_control
        # We focus on the immediate effect (post-treatment years)
        post_period = comparison_df[comparison_df[time] >= c]
        pre_period = comparison_df[comparison_df[time] < c]
        
        if not post_period.empty and not pre_period.empty:
            did_effect = post_period[y].mean() - pre_period[y].mean()
            results.append({'cohort': c, 'att': did_effect})
            
    att_df = pd.DataFrame(results)
    overall_att = att_df['att'].mean()
    
    print("\n" + "="*30)
    print("      CSDID SIMPLE REPORT      ")
    print("="*30)
    print(f"Aggregated ATT (Clean): {overall_att:.4f}")
    print(f"Number of Cohorts analyzed: {len(att_df)}")
    print("="*30)
    print("NOTE: This ATT only uses 'Never Treated' units as controls")
    print("to avoid the negative weight bias found in TWFE.")
    
    return att_df