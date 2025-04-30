from app import procesar_usuarios
import pandas as pd
import plotly.express as px

# Procesar los datos
data_usuarios, fechas_login = procesar_usuarios()

# Crear DataFrame principal
df_usuarios = pd.DataFrame(data_usuarios)

# Crear DataFrame de fechas
df_fechas = pd.DataFrame(fechas_login)

# Convertir fechas
df_fechas['fecha'] = pd.to_datetime(df_fechas['fecha'])

# Unir los dataframes
df_completo = df_usuarios.merge(df_fechas, left_on='id', right_on='id_usuarios', how='left')

# Calcular días inactivos
df_completo['dias_inactivo'] = (pd.Timestamp.now() - df_completo['fecha']).dt.days

# Mostrar resumen general
print(f"Cantidad total de cuentas: {len(df_completo)}\n")

activos = df_completo[df_completo['active_flag'] == True]
inactivos = df_completo[df_completo['active_flag'] == False]

print("===== RESUMEN GENERAL =====")
print(f"Total Usuarios: {len(df_completo)}")
print(f"Activos: {len(activos)}, Inactivos: {len(inactivos)}")
print(f"Sin login >7 días: {len(df_completo[df_completo['dias_inactivo'] > 7])}, >14 días: {len(df_completo[df_completo['dias_inactivo'] > 14])}, >30 días: {len(df_completo[df_completo['dias_inactivo'] > 30])}\n")

# Top 10 más inactivos
top_inactivos = df_completo.sort_values(by='dias_inactivo', ascending=False).head(10)
print(top_inactivos)
# Top 10 mas activos
top_activos = df_completo.sort_values(by='dias_inactivo', ascending=True).head(10)
print(top_activos)