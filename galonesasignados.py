import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import seaborn as sns
import json
from statsmodels.stats.multicomp import pairwise_tukeyhsd

# Asumiendo que tus datos ya están en un DataFrame llamado 'df'
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos2 = json.load(archivo)

# Imprimir los datos en la consola
df2 = pd.DataFrame(datos2)

# Realizar un ANOVA de una vía
modelo_anova2 = ols('GALONES_ASIGNADOS ~ C(NOMBRE_TIPO_UNIDAD)', data=df2).fit()
tabla_anova2 = sm.stats.anova_lm(modelo_anova2, typ=1)
print("Tabla ANOVA")
print(tabla_anova2)

# Prueba post-hoc de Bonferroni
resultado_bonferroni = pairwise_tukeyhsd(df2["GALONES_ASIGNADOS"], df2["NOMBRE_TIPO_UNIDAD"], alpha=0.05)
print("\nPrueba post-hoc de Bonferroni")
print(resultado_bonferroni.summary())

# Crear un boxplot agrupado por TIPO_UNIDAD para la columna GALONES_ASIGNADOS
sns.boxplot(x="NOMBRE_TIPO_UNIDAD", y="GALONES_ASIGNADOS", data=df2)

# Etiquetas de los ejes
plt.xlabel("NOMBRE_TIPO_UNIDAD")
plt.ylabel("GALONES_ASIGNADOS")

# Mostrar el gráfico
plt.show()