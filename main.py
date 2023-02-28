
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)

# Imprimir los datos en la consola
df = pd.DataFrame(datos)

# Obtener los intervalos de CANTIDAD_CONSUMIDA
bins = pd.interval_range(start=0, end=df["CANTIDAD_CONSUMIDA"].max(), freq=10)
marcas_clase = [interval.mid for interval in bins]

# Crear una nueva columna con la categoría a la que pertenece cada valor de CANTIDAD_CONSUMIDA
df["CANTIDAD_CONSUMIDA_CAT"] = pd.cut(df["CANTIDAD_CONSUMIDA"], bins)

# Obtener la frecuencia absoluta de cada categoría
freq_abs = pd.value_counts(df["CANTIDAD_CONSUMIDA_CAT"])

# Obtener la frecuencia acumulada de cada categoría
freq_cum = freq_abs.cumsum()

# Obtener la frecuencia relativa de cada categoría
freq_rel = freq_abs / len(df)

# Obtener la frecuencia relativa acumulada de cada categoría
freq_rel_cum = freq_rel.cumsum()

df_frec = pd.DataFrame({'Intervalos': bins, 'Frecuencia Absoluta': freq_abs})
df_frec['Marca de Clase'] = bins.mid
df_frec['Frecuencia Acumulada'] = df_frec['Frecuencia Absoluta'].cumsum()
df_frec['Frecuencia Relativa'] = df_frec['Frecuencia Absoluta'] / df_frec['Frecuencia Absoluta'].sum()
df_frec['Frecuencia Relativa Acumulada'] = df_frec['Frecuencia Acumulada'] / df_frec['Frecuencia Absoluta'].sum()
media = df['CANTIDAD_CONSUMIDA'].mean()
mediana = df['CANTIDAD_CONSUMIDA'].median()
moda = df['CANTIDAD_CONSUMIDA'].mode()[0]
print('Medidas de Tendencia Central:')
print('Media:', media)
print('Mediana:', mediana)
print('Moda:', moda)
print('\nDistribución de Frecuencias Agrupadas:')
print(df_frec)




plt.hist(df["CANTIDAD_CONSUMIDA"], bins=10)
plt.xlabel("CANTIDAD_CONSUMIDA")
plt.ylabel("Frecuencia")
plt.show()

# Polígono de frecuencias
sns.histplot(df, x="CANTIDAD_CONSUMIDA", kde=True, stat="density")
plt.xlabel("CANTIDAD_CONSUMIDA")
plt.ylabel("Frecuencia relativa")
plt.show()

# Medidas de dispersión
print("Desviación estándar:", np.std(df["CANTIDAD_CONSUMIDA"]))
print("Varianza:", np.var(df["CANTIDAD_CONSUMIDA"]))
print("Rango:", np.max(df["CANTIDAD_CONSUMIDA"]) - np.min(df["CANTIDAD_CONSUMIDA"]))
print("Rango intercuartil:", np.percentile(df["CANTIDAD_CONSUMIDA"], 75) - np.percentile(df["CANTIDAD_CONSUMIDA"], 25))

# Medidas de forma
print("Asimetría:", stats.skew(df["CANTIDAD_CONSUMIDA"]))
print("Curtosis:", stats.kurtosis(df["CANTIDAD_CONSUMIDA"]))

# Percentiles
print("Percentil 25:", np.percentile(df["CANTIDAD_CONSUMIDA"], 25))
print("Percentil 50 (Mediana):", np.percentile(df["CANTIDAD_CONSUMIDA"], 50))
print("Percentil 75:", np.percentile(df["CANTIDAD_CONSUMIDA"], 75))