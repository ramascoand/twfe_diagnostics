import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

def get_jakiela_weights(df, treatment, unit, time):
    """
    Calculates weights for TWFE decomposition based on Jakiela (2021).
    Formula: weight = resids / sum(resids^2)
    """
    # Regression: D ~ i.unit + i.time
    formula = f"{treatment} ~ C({unit}) + C({time})"
    resids = smf.ols(formula, data=df).fit().resid
    
    # Weight calculation
    t_variance = np.sum(resids**2)
    weights = resids / t_variance
    
    return weights

def get_weight_summary(df):
    """
    Provides a numerical summary of the calculated weights.
    Essential for identifying negative weights.
    """
    if 'weight' not in df.columns:
        return "Error: 'weight' column not found in DataFrame. Run get_jakiela_weights first."
    
    summary = {
        'Total Observations': len(df),
        'Positive Weights': (df['weight'] > 0).sum(),
        'Negative Weights': (df['weight'] < 0).sum(),
        'Mean Weight': df['weight'].mean(),
        'Min Weight': df['weight'].min(),
        'Max Weight': df['weight'].max(),
        'Sum of Weights': df['weight'].sum()
    }
    
    return pd.Series(summary)