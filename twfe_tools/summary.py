import pandas as pd

def get_weight_summary(df, weight_col='weight'):
    """
    Calculates statistical summary of TWFE weights, 
    identifying the prevalence of negative weights.
    """
    neg_weights = df[df[weight_col] < 0]
    pos_weights = df[df[weight_col] >= 0]
    
    summary = {
        'total_obs': len(df),
        'neg_count': len(neg_weights),
        'neg_share': len(neg_weights) / len(df) * 100,
        'neg_sum': neg_weights[weight_col].sum(),
        'pos_sum': pos_weights[weight_col].sum()
    }
    
    print(f"--- TWFE Weight Diagnostic ---")
    print(f"Negative weights found: {summary['neg_count']} ({summary['neg_share']:.2f}%)")
    print(f"Sum of negative weights: {summary['neg_sum']:.4f}")
    print(f"Sum of positive weights: {summary['pos_sum']:.4f}")
    
    return summary