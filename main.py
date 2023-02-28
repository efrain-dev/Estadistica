
import json
import pandas as pd

# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)

# Imprimir los datos en la consola
df = pd.DataFrame(datos);
#obtner intervalos 
# Agrupar los datos en intervalos utilizando la función pandas.cut()
bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # Definir los intervalos
labels = [f"{i}-{i+9}" for i in range(0, 100, 10)] # Definir las etiquetas de los intervalos
df['CANTIDAD_CONSUMIDA_INTERVALO'] = pd.cut(df['CANTIDAD_CONSUMIDA'], bins=bins, labels=labels, include_lowest=True)

# Obtener la distribución de frecuencias agrupadas utilizando la función pandas.value_counts()
distribucion_frecuencias = df['CANTIDAD_CONSUMIDA_INTERVALO'].value_counts(sort=False)


print(distribucion_frecuencias);