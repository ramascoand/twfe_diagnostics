from curses import window
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

def plot_event_study(df, y, unit, time, treatment_col):
    df = df.copy()
    
    # 1. Asegurar que el tiempo de tratamiento sea numérico
    df['first_treat'] = df.groupby(unit)[time].transform(lambda x: x[df[treatment_col] == 1].min())
    df['event_time'] = df[time] - df['first_treat']
    
    # Llenar NaNs en event_time para evitar que OLS los ignore (usamos un valor fuera del window)
    df['event_time_reg'] = df['event_time'].fillna(-999)
    
    # Definir ventana
    window = range(-5, 6)
    
    # --- TWFE LOGIC ---
    # Usamos Q() para nombres de columnas con espacios o caracteres especiales
    # Forzamos a que event_time sea tratado como categoría
    formula = f"Q('{y}') ~ C(event_time_reg, Treatment(reference=-1.0)) + C({unit}) + C({time})"
    
    try:
        twfe_model = smf.ols(formula, data=df).fit()
        # Extraer coeficientes buscando el patrón del nombre en el modelo
        twfe_effects = []
        for t in window:
            if t == -1:
                twfe_effects.append(0)
            else:
                # Buscamos el coeficiente correspondiente al tiempo t
                col_name = f"C(event_time_reg, Treatment(reference=-1.0))[T.{float(t)}]"
                twfe_effects.append(twfe_model.params.get(col_name, 0))
    except Exception as e:
        print(f"Error en TWFE: {e}")
        twfe_effects = [0] * len(window)

    # --- CSDID LOGIC (Simple Clean Comparison) ---
    # Comparar el cambio en tratados vs el cambio en nunca tratados
    csdid_effects = []
    never_treated = df[df['first_treat'].isna()]
    
    # Valor base (Pre-tratamiento en t=-1)
    base_treated_mean = df[df['event_time'] == -1][y].mean()
    base_control_mean = never_treated[y].mean()

    for t in window:
        if t == -1:
            csdid_effects.append(0)
            continue
        
        # Media de tratados en el tiempo relativo t
        treated_t = df[df['event_time'] == t][y].mean()
        
        # Media de los nunca tratados en los mismos años calendario en que los tratados están en t
        years_at_t = df[df['event_time'] == t][time].unique()
        control_t = never_treated[never_treated[time].isin(years_at_t)][y].mean()
        
        if pd.isna(treated_t) or pd.isna(control_t):
            csdid_effects.append(0)
        else:
            # Diff-in-Diff: (T_t - T_-1) - (C_t - C_-1)
            did = (treated_t - base_treated_mean) - (control_t - base_control_mean)
            csdid_effects.append(did)

    # --- PLOTTING ---
    plt.figure(figsize=(10, 6))
    plt.plot(window, twfe_effects, 'rs--', label='TWFE (Contaminated)', alpha=0.7)
    plt.plot(window, csdid_effects, 'bo-', label='CSDID (Clean)', linewidth=2)
    
    plt.axvline(-0.5, color='black', linestyle=':')
    plt.axhline(0, color='black', lw=1)
    plt.title(f"Diagnostic: Event Study for {y}")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.show()