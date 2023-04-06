import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from scipy.stats import shapiro
from scipy.stats import f_oneway
import collections
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)


# Create a Pandas DataFrame from the JSON data
df = pd.DataFrame.from_records(datos)

# Calcular la curtosis de la columna TOTAL_CONSUMIDO para el tipo de combustible DIESEL
curtosis_diesel = df[df['COMBUSTIBLE'] == 'DIESEL']['TOTAL_CONSUMIDO'].kurtosis()

# Calcular la curtosis de la columna TOTAL_CONSUMIDO para el tipo de combustible REGULAR
curtosis_regular = df[df['COMBUSTIBLE'] == 'REGULAR']['TOTAL_CONSUMIDO'].kurtosis()

# Imprimir la curtosis para ambos tipos de combustible
print(f"Curtosis para el tipo de combustible DIESEL: {curtosis_diesel}")
print(f"Curtosis para el tipo de combustible REGULAR: {curtosis_regular}")

diesel_total = 0
regular_total = 0
    
# Calcular el total consumido por tipo de combustible
for item in datos:
    if item["COMBUSTIBLE"] == "DIESEL":
        diesel_total += item["TOTAL_CONSUMIDO"]
    elif item["COMBUSTIBLE"] == "REGULAR":
        regular_total += item["TOTAL_CONSUMIDO"]

# Crear la gráfica
fig, axs = plt.subplots(1, 2, figsize=(10, 5))
axs[0].hist(df.loc[df['COMBUSTIBLE'] == 'DIESEL', 'TOTAL_CONSUMIDO'], bins=10)
axs[0].set_title('DIESEL')
axs[1].hist(df.loc[df['COMBUSTIBLE'] == 'REGULAR', 'TOTAL_CONSUMIDO'], bins=10)
axs[1].set_title('REGULAR')
# plt.show()

df.boxplot(column='TOTAL_CONSUMIDO', by='COMBUSTIBLE')

# Obtener la variable "TOTAL_CONSUMIDO" como una lista
total_consumido = [d["TOTAL_CONSUMIDO"] for d in datos]

# Calcular medidas estadísticas
media = np.mean(total_consumido)
mediana = np.median(total_consumido)
desv_est = np.std(total_consumido)
pct_25 = np.percentile(total_consumido, 25)
pct_75 = np.percentile(total_consumido, 75)

# Imprimir resultados
print(f"Media: {media:.2f}")
print(f"Mediana: {mediana:.2f}")
print(f"Desviación estándar: {desv_est:.2f}")
print(f"Percentil 25: {pct_25:.2f}")
print(f"Percentil 75: {pct_75:.2f}")

data = pd.read_json("datos.json")

# Agrupar los datos por estación y calcular estadísticas de galones asignados
estacion_stats = data.groupby("NOMBRE_ESTACION")["GALONES_ASIGNADOS"].agg(['mean', 'std', 'min', 'max'])

print(estacion_stats)
df = pd.DataFrame(datos)
percentiles = df.groupby('NOMBRE_ESTACION')['GALONES_ASIGNADOS'].quantile([0.05, 0.10, 0.25, 0.50, 0.75, 0.90, 0.95]).unstack()

print("PERCENTILES DE GALONES ASIGNADOS POR ESTACIÓN")
print("-" * 75)
print(percentiles)


galones_asignados = [d['GALONES_ASIGNADOS'] for d in datos]
total_consumido = [d['TOTAL_CONSUMIDO'] for d in datos]

plt.plot(galones_asignados, total_consumido, 'bo')
plt.xlabel('Galones Asignados')
plt.ylabel('Total Consumido')
plt.show()



result = f_oneway(df[df['USUARIO_ASIGNACION'] == '33-USER']['PRECIO_COMBUSTIBLE'],
                   df[df['USUARIO_ASIGNACION'] == '20-USER']['PRECIO_COMBUSTIBLE'])

# Imprimir el resultado del ANOVA
print('Estadístico de prueba:', result.statistic)
print('Valor p:', result.pvalue)

if result.pvalue > 0.05:
    print('No hay diferencias significativas en los precios de combustible asignados por diferentes usuarios.')
else:
    print('Hay diferencias significativas en los precios de combustible asignados por diferentes usuarios.')
    
# Realizar el análisis de Tukey
tukey = pairwise_tukeyhsd(df['PRECIO_COMBUSTIBLE'], df['USUARIO_ASIGNACION'], 0.05)

# Imprimir el resultado del análisis de Tukey
print(tukey.summary())

datos_por_tipo = {}

for d in datos:
    tipo_combustible = d["COMBUSTIBLE"]
    precio_combustible = d["PRECIO_COMBUSTIBLE"]
    if tipo_combustible not in datos_por_tipo:
        datos_por_tipo[tipo_combustible] = []
    datos_por_tipo[tipo_combustible].append(precio_combustible)
    
plt.boxplot([datos_por_tipo["DIESEL"], datos_por_tipo["REGULAR"]])
plt.xlabel("Tipo de combustible")
plt.ylabel("Precio (USD)")
plt.xticks([1, 2], ["DIESEL", "REGULAR"])
plt.show()



precios_por_combustible = df.groupby('COMBUSTIBLE')['PRECIO_COMBUSTIBLE'].mean()

# imprimir los precios por tipo de combustible
print(precios_por_combustible)

fig, ax = plt.subplots()

# generar una lista de colores para la gráfica de pie
colores = ['#FFC107', '#2196F3', '#4CAF50', '#FF5722']

# graficar la gráfica de pie con los precios por tipo de combustible
ax.pie(precios_por_combustible, labels=precios_por_combustible.index, colors=colores, autopct='%1.1f%%')

# agregar título y leyenda a la gráfica
ax.set_title('Precios por tipo de combustible')
ax.legend(title='Combustible', loc='center left', bbox_to_anchor=(1, 0.5))

# mostrar la gráfica
plt.show()

# cargamos los datos
with open('datos.json') as f:
    data = json.load(f)


# Crear un diccionario para almacenar los precios totales por tipo de combustible
prices = collections.defaultdict(float)
for d in data:
    prices[d['COMBUSTIBLE']] += d['PRECIO_COMBUSTIBLE'] * d['CANTIDAD_CONSUMIDA']

# Obtener los 10 tipos de combustibles más comunes
common_fuels = sorted(prices.items(), key=lambda x: x[1], reverse=True)[:10]

# Resumir los precios de los 10 tipos de combustibles más comunes
fuel_names = [x[0] for x in common_fuels]
fuel_prices = [x[1] for x in common_fuels]

# Generar el gráfico de pie
plt.pie(fuel_prices, labels=fuel_names, autopct='%1.1f%%')
plt.title('Precios totales por tipo de combustible')
plt.show()


combustibles = {}

for registro in data:
    combustible = registro["COMBUSTIBLE"]
    precio = registro["PRECIO_COMBUSTIBLE"]
    cantidad_consumida = registro["CANTIDAD_CONSUMIDA"]
        
    if combustible not in combustibles:
        combustibles[combustible] = {}
    
    if precio not in combustibles[combustible]:
        combustibles[combustible][precio] = 0
    
    combustibles[combustible][precio] += cantidad_consumida

for combustible, precios in combustibles.items():
    labels = []
    sizes = []

    for precio, cantidad in precios.items():
        labels.append(f"{combustible} - {precio}")
        sizes.append(cantidad)

    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(f"Gráfica de pastel para {combustible}")
    plt.axis('equal')
    plt.show()
    
# agrupar datos por tipo de combustible
combustibles = {}
for dato in datos:
    if dato["COMBUSTIBLE"] not in combustibles:
        combustibles[dato["COMBUSTIBLE"]] = []
    combustibles[dato["COMBUSTIBLE"]].append(dato)

# crear gráficos para cada tipo de combustible
for combustible, datos_combustible in combustibles.items():
    # dividir datos en segmentos de precios
    precios = [dato["PRECIO_COMBUSTIBLE"] for dato in datos_combustible]
    segmentos, bordes = np.histogram(precios, bins=10) # cambiar el valor del parámetro "bins" según se desee
    
    # crear gráfico de bloques segmentados
    plt.figure()
    plt.hist(precios, bins=bordes)
    plt.title(f"Segmentos de precios de {combustible}")
    plt.xlabel("Precio del combustible")
    plt.ylabel("Cantidad de datos")
    plt.show()