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

# Obtener los intervalos de PRECIO_COMBUSTIBLE
bins = pd.interval_range(start=30, end=df["PRECIO_COMBUSTIBLE"].max()+1, freq=1)
marcas_clase = [interval.mid for interval in bins]

# Crear una nueva columna con la categoría a la que pertenece cada valor de PRECIO_COMBUSTIBLE
df["PRECIO_COMBUSTIBLE_CAT"] = pd.cut(df["PRECIO_COMBUSTIBLE"], bins)

# Obtener la frecuencia absoluta de cada categoría
freq_abs = pd.value_counts(df["PRECIO_COMBUSTIBLE_CAT"])

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
media = df['PRECIO_COMBUSTIBLE'].mean()
mediana = df['PRECIO_COMBUSTIBLE'].median()
moda = df['PRECIO_COMBUSTIBLE'].mode()[0]
print('Medidas de Tendencia Central:')
print('Media:', media)
print('Mediana:', mediana)
print('Moda:', moda)
print('\nDistribución de Frecuencias Agrupadas:')
print(df_frec)

# Histograma de frecuencias
plt.hist(df["PRECIO_COMBUSTIBLE"], bins=10)
plt.xlabel("PRECIO_COMBUSTIBLE")
plt.ylabel("Frecuencia")
plt.show()

# Polígono de frecuencias
sns.histplot(df, x="PRECIO_COMBUSTIBLE", kde=True, stat="density")
plt.xlabel("PRECIO_COMBUSTIBLE")
plt.ylabel("Frecuencia relativa")
plt.show()

# Medidas de dispersión
print("Desviación estándar:", np.std(df["PRECIO_COMBUSTIBLE"]))
print("Varianza:", np.var(df["PRECIO_COMBUSTIBLE"]))
print("Rango:", np.max(df["PRECIO_COMBUSTIBLE"]) - np.min(df["PRECIO_COMBUSTIBLE"]))
print("Rango intercuartil:", np.percentile(df["PRECIO_COMBUSTIBLE"], 75) - np.percentile(df["PRECIO_COMBUSTIBLE"], 25))

# Medidas de forma
print("Asimetría:", stats.skew(df["PRECIO_COMBUSTIBLE"]))
print("Curtosis:", stats.kurtosis(df["PRECIO_COMBUSTIBLE"]))

# Percentiles
print("Percentil 25:", np.percentile(df["PRECIO_COMBUSTIBLE"], 25))
print("Percentil 50 (Mediana):", np.percentile(df["PRECIO_COMBUSTIBLE"], 50))
print("Percentil 75:", np.percentile(df["PRECIO_COMBUSTIBLE"], 75))