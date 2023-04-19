import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
import json
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import pingouin as pg
from statsmodels.stats.anova import AnovaRM

# Asumiendo que tus datos ya están en un DataFrame llamado 'df'
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)

# Imprimir los datos en la consola
df = pd.DataFrame(datos)


# Transformar los datos al formato largo
df_largo = df.melt(id_vars=['ID_TIPO_UNIDAD', 'ID_UNIDAD'], value_vars=['GALONES_ASIGNADOS', 'TOTAL_CONSUMIDO'], var_name='factor1', value_name='MEASURE_1')

# Realizar un ANOVA de medidas repetidas mixto
mixed_anova_results = pg.mixed_anova(data=df_largo, dv='MEASURE_1', within='factor1', subject='ID_UNIDAD', between='ID_TIPO_UNIDAD')

# Imprimir los resultados del ANOVA
print(mixed_anova_results)

# Crear un boxplot
plt.figure(figsize=(12, 6))
sns.boxplot(x='factor1', y='MEASURE_1', hue='ID_TIPO_UNIDAD', data=df_largo)
plt.xlabel('Factor1 (GALONES_ASIGNADOS y TOTAL_CONSUMIDO)')
plt.ylabel('MEASURE_1')
plt.title('Boxplot de MEASURE_1 por factor1 y ID_TIPO_UNIDAD')
plt.legend(title='ID TIPO UNIDAD')
plt.show()
