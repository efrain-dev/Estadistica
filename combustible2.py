from scipy.stats import f_oneway, shapiro
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
from scipy.stats import levene,ttest_ind
import pandas as pd
import scipy.stats as stats

import json

# datos de ejemplo (asumiendo que esta es la variable que contiene los datos)
# cargamos los datos
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json') as f:
    datos = json.load(f)
    

# análisis de normalidad
galones_asignados = [dato["GALONES_ASIGNADOS"] for dato in datos]
usuario_asignacion = [int(dato["ID_USUARIO_ASIGNACION"]) for dato in datos]

sw_galones, p_galones = shapiro(galones_asignados)
sw_usuario, p_usuario = shapiro(usuario_asignacion)

if p_galones > 0.5 and p_usuario > 0.5:
    print("Los datos siguen una distribución normal.")
else:
    print("Los datos no siguen una distribución normal. Se sugiere realizar una transformación de los datos o usar pruebas no paramétricas.")

# prueba F
f_val, p_val = f_oneway(galones_asignados, usuario_asignacion)
if p_val < 0.05:
    print("La prueba F indica que hay una diferencia significativa entre las medias de los grupos.")
else:
    print("La prueba F no indica que haya una diferencia significativa entre las medias de los grupos.")
# Seleccionar los datos a graficar

# Obtener los datos de galones asignados y total consumido
galones = [dato["GALONES_ASIGNADOS"] for dato in datos]
consumido = [dato["TOTAL_CONSUMIDO"] for dato in datos]

# Crear la gráfica de puntos
plt.scatter(consumido, galones)

# Agregar título y etiquetas de los ejes
plt.title("Gráfica de puntos de Galones asignados vs Total consumido")
plt.xlabel("Total consumido")
plt.ylabel("Galones asignados")

# Mostrar la gráfica
plt.show()


# separar los datos de galones asignados en dos grupos según el tipo de combustible
galones_gasolina = [d['GALONES_ASIGNADOS'] for d in datos if d['COMBUSTIBLE'] == 'GASOLINA']
galones_diesel = [d['GALONES_ASIGNADOS'] for d in datos if d['COMBUSTIBLE'] == 'DIESEL']

# realizar la prueba T
t, p = ttest_ind(galones_gasolina, galones_diesel, equal_var=False)

# imprimir el resultado de la prueba T
if p < 0.05:
    print("Hay evidencia estadística de que los galones asignados y el tipo de combustible están correlacionados.")
else:
    print("No hay suficiente evidencia estadística para afirmar que los galones asignados y el tipo de combustible están correlacionados.")
    
    
# Crear un DataFrame a partir de la estructura de datos
df = pd.DataFrame(datos)

# Agrupar los datos por tipo de combustible y calcular la media y desviación estándar de los galones asignados
grouped = df.groupby('COMBUSTIBLE')['GALONES_ASIGNADOS'].agg(['mean', 'std', 'count'])

# Calcular la prueba T para las muestras no pareadas con varianzas desiguales
t, p = ttest_ind(df.loc[df['COMBUSTIBLE'] == 'DIESEL', 'GALONES_ASIGNADOS'], 
                 df.loc[df['COMBUSTIBLE'] == 'REGULAR', 'GALONES_ASIGNADOS'], 
                 equal_var=False)

# Mostrar los resultados
print('Group Statistics\n')
print(grouped.to_string())
print('\nIndependent Samples T-Test\n')
print(f'T-Statistic: {t:.2f}\nP-Value: {p:.4f}')


# Crear listas separadas para cada tipo de combustible
diesel_galones = [d['GALONES_ASIGNADOS'] for d in datos if d['COMBUSTIBLE'] == 'DIESEL']
regular_galones = [d['GALONES_ASIGNADOS'] for d in datos if d['COMBUSTIBLE'] == 'REGULAR']

# Realizar prueba de Levene para la igualdad de varianzas
levene_test = levene(diesel_galones, regular_galones)
print("Levene's Test for Equality of Variances:")
print("F =", levene_test.statistic)
print("p =", levene_test.pvalue)

# Realizar prueba T para la igualdad de medias
t_test = ttest_ind(diesel_galones, regular_galones, equal_var=False)
print("\nt-test for Equality of Means:")
print("t =", t_test.statistic)
print("p =", t_test.pvalue)

# Ejecutar el análisis ANOVA
modelo = ols('GALONES_ASIGNADOS ~ COMBUSTIBLE', data=df).fit()
tabla_anova = sm.stats.anova_lm(modelo, typ=2)

# Imprimir la tabla ANOVA
print(tabla_anova)

# Agregar una columna para contar la cantidad de galones asignados por usuario de asignación
galones_por_usuario = df.groupby('USUARIO_ASIGNACION')['GALONES_ASIGNADOS'].sum().reset_index()

# Crear el gráfico de barras
plt.bar(galones_por_usuario['USUARIO_ASIGNACION'], galones_por_usuario['GALONES_ASIGNADOS'])

# Añadir título y etiquetas de los ejes
plt.title('Cantidad de Galones Asignados por Usuario de Asignación')
plt.xlabel('Usuario de Asignación')
plt.ylabel('Galones Asignados')

# Mostrar el gráfico
plt.show()
# Convertir la columna 'FECHA_ASIGNACION' en formato datetime
df['FECHA_ASIGNACION'] = pd.to_datetime(df['FECHA_ASIGNACION'])

# Agregar una columna para contar la cantidad de galones asignados por usuario de asignación y por fecha
galones_por_usuario_y_fecha = df.groupby(['USUARIO_ASIGNACION', 'FECHA_ASIGNACION'])['GALONES_ASIGNADOS'].sum().reset_index()

# Crear un DataFrame separado para cada usuario de asignación y convertir la columna de fechas en el índice
usuarios = galones_por_usuario_y_fecha['USUARIO_ASIGNACION'].unique()
dfs = []
for usuario in usuarios:
    df_usuario = galones_por_usuario_y_fecha[galones_por_usuario_y_fecha['USUARIO_ASIGNACION'] == usuario]
    df_usuario = df_usuario.set_index('FECHA_ASIGNACION')
    dfs.append(df_usuario)

# Crear el gráfico de líneas
fig, ax = plt.subplots()
for i, df_usuario in enumerate(dfs):
    ax.plot(df_usuario.index, df_usuario['GALONES_ASIGNADOS'], label=usuarios[i])

# Añadir título y etiquetas de los ejes
plt.title('Cantidad de Galones Asignados por Usuario de Asignación')
plt.xlabel('Fecha de Asignación')
plt.ylabel('Galones Asignados')

# Añadir una leyenda
ax.legend()

# Mostrar el gráfico
plt.show()



# Filtrar los datos para incluir sólo los precios de combustible en diciembre de 2022, enero de 2023 y febrero de 2023
combustible_diciembre = df.loc[(df['FECHA_CONSUMO'].str.contains('12\/')) & (df['PRECIO_COMBUSTIBLE'] > 0), 'PRECIO_COMBUSTIBLE']
combustible_enero = df.loc[(df['FECHA_CONSUMO'].str.contains('1\/')) & (df['PRECIO_COMBUSTIBLE'] > 0), 'PRECIO_COMBUSTIBLE']
combustible_febrero = df.loc[(df['FECHA_CONSUMO'].str.contains('2\/')) & (df['PRECIO_COMBUSTIBLE'] > 0), 'PRECIO_COMBUSTIBLE']

# Calcular la media y la desviación estándar de los precios de combustible de los tres meses
media_combustible = combustible_diciembre.mean()
std_combustible = combustible_diciembre.std()

# Calcular la estadística Z para enero y febrero en comparación con la media de diciembre
z_enero = (combustible_enero.mean() - media_combustible) / (std_combustible / (len(combustible_enero) ** 0.5))
z_febrero = (combustible_febrero.mean() - media_combustible) / (std_combustible / (len(combustible_febrero) ** 0.5))

# Realizar una prueba de hipótesis sobre si la media de los precios es significativamente diferente de un valor de referencia de 35.97
valor_referencia = 35.97
p_valor = stats.ttest_1samp(combustible_diciembre, valor_referencia)[1]

# Imprimir los resultados
print(f"Estadística Z para enero: {z_enero:.3f}")
print(f"Estadística Z para febrero: {z_febrero:.3f}")
print(f"P-valor para la prueba de hipótesis: {p_valor:.3f}")


precios_combustible = df.loc[df['PRECIO_COMBUSTIBLE'] > 0, 'PRECIO_COMBUSTIBLE']

# Calcular la media y la desviación estándar de los precios de combustible
media_combustible = precios_combustible.mean()
std_combustible = precios_combustible.std()

# Calcular la estadística Z para cada observación de precio de combustible
z_precios_combustible = (precios_combustible - media_combustible) / std_combustible

# Imprimir estadísticas descriptivas de la estadística Z
print(f"Zscore: PRECIO COMBUSTIBLE\n\nN = {len(z_precios_combustible)}\nValid = {len(z_precios_combustible)}\nMissing = 0\n")
print(z_precios_combustible.describe().to_string() + "\n")

# Crear una tabla de frecuencias para los valores de la estadística Z
frecuencias_z = pd.cut(z_precios_combustible, [-float('inf'), -1.9, -1.6, -1.3, -1.1, -0.98, -0.9, -0.84, -0.76, -0.7, -0.56, -0.48, -0.2, 0.01, 0.15, 0.22, 0.36, 0.51, 0.86, 0.93, 1.14, 1.21, 1.28, 1.35, float('inf')])
frecuencias_z = frecuencias_z.value_counts(sort=False).to_frame().reset_index()
frecuencias_z.columns = ['Intervalo Z', 'Frecuencia']
frecuencias_z['%'] = (frecuencias_z['Frecuencia'] / len(z_precios_combustible)) * 100

# Imprimir la tabla de frecuencias
print("Zscore: PRECIO COMBUSTIBLE\n")
print(frecuencias_z.to_string(index=False))



# Filtrar los datos para incluir sólo los precios de combustible que son mayores que cero
precios_combustible = df.loc[df['PRECIO_COMBUSTIBLE'] > 0, 'PRECIO_COMBUSTIBLE']

# Calcular la media y la desviación estándar de los precios de combustible
media_combustible = precios_combustible.mean()
std_combustible = precios_combustible.std()

# Calcular la estadística Z para cada observación de precio de combustible
z_precios_combustible = (precios_combustible - media_combustible) / std_combustible

# Crear una tabla de frecuencias para los valores de la estadística Z

frecuencias_z = pd.cut(z_precios_combustible, [-float('inf'), -1.9, -1.6, -1.3, -1.1, -0.98, -0.9, -0.84, -0.76, -0.7, -0.56, -0.48, -0.2, 0.01, 0.15, 0.22, 0.36, 0.51, 0.86, 0.93, 1.14, 1.21, 1.28, 1.35, float('inf')])
frecuencias_z = frecuencias_z.value_counts(sort=False).to_frame().reset_index()
frecuencias_z.columns = ['Intervalo Z', 'Frecuencia']
frecuencias_z['Intervalo Z'] = frecuencias_z['Intervalo Z'].astype(str)

# Graficar una gráfica de barras que muestre la cantidad de observaciones en cada intervalo de valores de Z
plt.bar(frecuencias_z['Intervalo Z'], frecuencias_z['Frecuencia'])
plt.title('Frecuencia de valores Z del precio del combustible')
plt.xlabel('Intervalo Z')
plt.ylabel('Frecuencia')
plt.show()
