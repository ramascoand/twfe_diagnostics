# CONFIGURACIÓN DEL USUARIO
FILE_PATH = "data/WDI-FPE-data.dta"
OUTCOME = "primary"      # Aquí el usuario pone su 'y'
TREATMENT = "treatment"  # Aquí su 'd'
ENTITY = "id"            # Aquí su 'i'
TIME = "year"            # Aquí su 't'

# EJECUCIÓN AUTOMÁTICA
df = pd.read_stata(FILE_PATH)
df['weight'] = get_jakiela_weights(df, TREATMENT, ENTITY, TIME)

# Todo lo demás usa las variables de arriba
print(run_slope_test(df, OUTCOME, TREATMENT, ENTITY, TIME))