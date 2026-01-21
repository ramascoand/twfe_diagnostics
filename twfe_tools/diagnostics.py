import pandas as pd
import numpy as np
from linearmodels.panel import PanelOLS
import statsmodels.formula.api as smf

class TWFEDiagnostic:
    """
    Class to perform diagnostics on Two-Way Fixed Effects models.
    Encapsulates Slope Test, Robust TWFE, and CSDID logic.
    """
    def __init__(self, df, y_col, d_col, unit_col, time_col):
        self.df = df.copy()
        self.y_col = y_col
        self.d_col = d_col
        self.unit_col = unit_col
        self.time_col = time_col

    def run_slope_test(self):
        """Performs the Jakiela (2021) Slope Test."""
        # Ensure weights exist
        if 'weight' not in self.df.columns:
            raise ValueError("Weights not found. Please calculate weights and add them to the dataframe first.")
            
        # Create outcome difference
        self.df = self.df.sort_values([self.unit_col, self.time_col])
        self.df['outcome_diff'] = self.df.groupby(self.unit_col)[self.y_col].diff()
        
        # Regression of outcome diffs on weights
        formula = "outcome_diff ~ weight"
        model = smf.ols(formula, data=self.df).fit()
        return model.summary()

    def run_robust_comparison(self):
        """Standard TWFE with Clustered Robust Errors."""
        df_panel = self.df.set_index([self.unit_col, self.time_col])
        # Use Q() for column names to handle special characters or spaces
        formula = f"Q('{self.y_col}') ~ Q('{self.d_col}') + EntityEffects + TimeEffects"
        model = PanelOLS.from_formula(formula, data=df_panel).fit(cov_type='clustered', cluster_entity=True)
        return model

    def run_csdid_simple(self):
        """Simplified Callaway & Sant'Anna (2021) estimator."""
        df_temp = self.df.copy()
        df_temp['first_treat'] = df_temp.groupby(self.unit_col)[self.time_col].transform(
            lambda x: x[df_temp[self.d_col] == 1].min()
        )
        
        cohorts = df_temp['first_treat'].dropna().unique()
        results = []
        
        for c in cohorts:
            # Group treated in this cohort
            treated_group = df_temp[df_temp['first_treat'] == c]
            
            # CONTROL GROUP: Never treated OR not yet treated at time 'c'
            control_group = df_temp[
                (df_temp['first_treat'].isna()) | (df_temp['first_treat'] > c)
            ]
            
            if control_group.empty:
                continue

            # DiD components
            t_post = treated_group[treated_group[self.time_col] >= c][self.y_col].mean()
            t_pre  = treated_group[treated_group[self.time_col] < c][self.y_col].mean()
            
            c_post = control_group[control_group[self.time_col] >= c][self.y_col].mean()
            c_pre  = control_group[control_group[self.time_col] < c][self.y_col].mean()
            
            if pd.notna(t_post) and pd.notna(c_post):
                att = (t_post - t_pre) - (c_post - c_pre)
                results.append({'cohort': c, 'att': att})
                
        # Handle the case where no cohorts could be estimated
        if not results:
            print("⚠️ Warning: No valid control groups found for CSDID. Check your treatment variable.")
            return pd.DataFrame(columns=['cohort', 'att'])
            
        return pd.DataFrame(results)