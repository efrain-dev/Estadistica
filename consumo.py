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

# Obtener los intervalos de TOTAL_CONSUMIDO
bins = pd.interval_range(start=0, end=df["TOTAL_CONSUMIDO"].max(), freq=340)
marcas_clase = [interval.mid for interval in bins]

# Crear una nueva columna con la categoría a la que pertenece cada valor de TOTAL_CONSUMIDO
df["TOTAL_CONSUMIDO_CAT"] = pd.cut(df["TOTAL_CONSUMIDO"], bins)

# Obtener la frecuencia absoluta de cada categoría
freq_abs = pd.value_counts(df["TOTAL_CONSUMIDO_CAT"])

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
media = df['TOTAL_CONSUMIDO'].mean()
mediana = df['TOTAL_CONSUMIDO'].median()
moda = df['TOTAL_CONSUMIDO'].mode()[0]
print('Medidas de Tendencia Central:')
print('Media:', media)
print('Mediana:', mediana)
print('Moda:', moda)
print('\nDistribución de Frecuencias Agrupadas:')
print(df_frec)

# Histograma de frecuencias
plt.hist(df["TOTAL_CONSUMIDO"], bins=10)
plt.xlabel("TOTAL_CONSUMIDO")
plt.ylabel("Frecuencia")
plt.show()

# Polígono de frecuencias
sns.histplot(df, x="TOTAL_CONSUMIDO", kde=True, stat="density")
plt.xlabel("TOTAL_CONSUMIDO")
plt.ylabel("Frecuencia relativa")
plt.show()

# Medidas de dispersión
print("Desviación estándar:", np.std(df["TOTAL_CONSUMIDO"]))
print("Varianza:", np.var(df["TOTAL_CONSUMIDO"]))
print("Rango:", np.max(df["TOTAL_CONSUMIDO"]) - np.min(df["TOTAL_CONSUMIDO"]))
print("Rango intercuartil:", np.percentile(df["TOTAL_CONSUMIDO"], 75) - np.percentile(df["TOTAL_CONSUMIDO"], 25))

# Medidas de forma
print("Asimetría:", stats.skew(df["TOTAL_CONSUMIDO"]))
print("Curtosis:", stats.kurtosis(df["TOTAL_CONSUMIDO"]))

# Percentiles
print("Percentil 25:", np.percentile(df["TOTAL_CONSUMIDO"], 25))
print("Percentil 50 (Mediana):", np.percentile(df["TOTAL_CONSUMIDO"], 50))
print("Percentil 75:", np.percentile(df["TOTAL_CONSUMIDO"], 75))