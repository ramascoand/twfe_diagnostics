# TWFE Diagnostics for Staggered Adoption

This repository provides tools to diagnose potential biases in Two-Way Fixed Effects (TWFE) models when treatment timing is staggered.

## Features
- **Jakiela (2021) Weight Decomposition:** Identify negative weights that can bias TWFE estimates.
- **Robustness Comparison:** Automated comparison between standard TWFE and the Callaway & Sant'Anna (2021) CSDID estimator.
- **Visual Diagnostics:** Ready-to-use plotting tools for weight distributions.

## How to use
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`.
3. Open `analysis.ipynb` to see the full diagnostic workflow.

## Credits
Based on the econometric logic of Jakiela (2021) and Callaway & Sant'Anna (2021).