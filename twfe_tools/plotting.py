import matplotlib.pyplot as plt
import seaborn as sns

def plot_weights_histogram(df):
    """
    Replicate  histograms from FPE-weights-histograms-2021-03-24.do
    Show the distribution of weights for the control and treatment groups.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(data=df[df['treatment'] == 0], x='weight', color='red', 
                 label='Comparison Group', kde=True, stat="proportion", alpha=0.4)
    sns.histplot(data=df[df['treatment'] == 1], x='weight', color='blue', 
                 label='Treatment Group', kde=True, stat="proportion", alpha=0.6)

    plt.axvline(0, color='black', linestyle='--')
    plt.title("Distribution of TWFE Weights: Treated vs. Control Groups")
    plt.legend()
    plt.show()

def plot_diagnostic_heatmap(df, unit_col, time_col):
    """
    Replicate  logic from FPE-heatmap-2021-03-24.do
    Create a scatter plot that functions as a heatmap to identify negative weights.
    """
    # Definir categorías de diagnóstico
    df['status'] = 'Comparison'
    df.loc[(df['treatment'] == 1) & (df['weight'] > 0), 'status'] = 'Treated (+ weight)'
    df.loc[(df['treatment'] == 1) & (df['weight'] < 0), 'status'] = 'Treated (- weight)'

    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=df, x=time_col, y=unit_col, hue='status', 
                    palette={'Comparison': 'lightgrey', 
                             'Treated (+ weight)': 'orange', 
                             'Treated (- weight)': 'darkred'},
                    marker='s', s=100)

    plt.title("Diagnostics Map: Identification of Negative Weights by Year/Unit")
    plt.legend(title="State")
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.show()