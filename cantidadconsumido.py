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

# Asumiendo que tus datos ya están en un DataFrame llamado 'df'
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)

# Imprimir los datos en la consola
df = pd.DataFrame(datos)

# Realizar un ANOVA de una vía
modelo_anova = ols('CANTIDAD_CONSUMIDA ~ C(NOMBRE_TIPO_UNIDAD)', data=df).fit()
tabla_anova = sm.stats.anova_lm(modelo_anova, typ=1)
print("Tabla ANOVA")
print(tabla_anova)

# Realizar la prueba post-hoc de Games-Howell
games_howell = pg.pairwise_gameshowell(data=df, dv="CANTIDAD_CONSUMIDA", between="NOMBRE_TIPO_UNIDAD")

# Mostrar los resultados
print("Resultados de la prueba post-hoc de Games-Howell:")
print(games_howell)

# Crear un boxplot agrupado por TIPO_UNIDAD para la columna CANTIDAD_CONSUMIDA
sns.boxplot(x="NOMBRE_TIPO_UNIDAD", y="CANTIDAD_CONSUMIDA", data=df)

# Etiquetas de los ejes
plt.xlabel("NOMBRE_TIPO_UNIDAD")
plt.ylabel("CANTIDAD_CONSUMIDA")

# Mostrar el gráfico
plt.show()

