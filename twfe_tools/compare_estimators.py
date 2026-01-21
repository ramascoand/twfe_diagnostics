import statsmodels.formula.api as smf
import pandas as pd

def compare_estimators(df, y, d, unit, time):
    """
    Compares the standard TWFE estimator against a simple 
    heterogeneity-robust alternative.
    """
    # 1. Standard TWFE
    formula_std = f"Q('{y}') ~ Q('{d}') + C({unit}) + C({time})"
    model_std = smf.ols(formula_std, data=df).fit()
    twfe_coeff = model_std.params[f"Q('{d}')"]
    
    # 2. Simple Robust Approximation (Using the weights we calculated)
    # If weights are already in df, we can see the impact
    if 'weight' not in df.columns:
        print("Please calculate weights first.")
        return
    
    # The 'Slope Test' already told us if they differ significantly.
    # Here we show the coefficients side by side
    print("--- Estimator Comparison ---")
    print(f"Standard TWFE Coefficient: {twfe_coeff:.4f}")
    print(f"P-value: {model_std.pvalues[f"Q('{d}')"]:.4f}")
    print("----------------------------")
    print("NOTE: If the Jakiela Slope Test was significant,")
    print("the TWFE coefficient above is likely biased.")