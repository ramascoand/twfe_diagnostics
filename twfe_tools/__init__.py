# --- twfe_tools/__init__.py ---

# Import the main Diagnostic Class
from .diagnostics import TWFEDiagnostic

# Import standalone functions for convenience
from .weights import get_jakiela_weights, get_weight_summary
from .plotting import plot_weights_histogram

# If you want to keep these functions available outside the class 
# (only if you didn't delete them from diagnostics.py)
#from .diagnostics import run_slope_test, run_robust_comparison, run_csdid_simple

# From event_study.py (Dynamics)
#from .event_study import plot_event_study

# From robust_estimators.py (CSDID and Robust logic)
from .robust_estimators import run_robust_comparison
from .robust_estimators import run_csdid_simple