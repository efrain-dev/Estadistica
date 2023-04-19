import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.multivariate.manova import MANOVA
import json
from statsmodels.formula.api import ols

# Asumiendo que tus datos ya están en un DataFrame llamado 'df'
# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)

# Imprimir los datos en la consola
df = pd.DataFrame(datos)


# Realizar un análisis MANOVA
manova = MANOVA.from_formula('CANTIDAD_CONSUMIDA + PRECIO_COMBUSTIBLE ~ COMBUSTIBLE', data=df)
manova_resultados = manova.mv_test()

# Mostrar los resultados
print("Resultados de la prueba MANOVA:")
print(manova_resultados)


# Asegúrate de que los nombres de las columnas en tu DataFrame sean correctos
df_clean = df.dropna(subset=['CANTIDAD_CONSUMIDA', 'PRECIO_COMBUSTIBLE', 'COMBUSTIBLE'])

# Realizar un ANOVA de dos vías utilizando la fórmula de regresión
model = ols('CANTIDAD_CONSUMIDA ~ C(COMBUSTIBLE) * C(PRECIO_COMBUSTIBLE)', data=df_clean).fit()

# Mostrar los resultados de la tabla ANOVA
anova_table = sm.stats.anova_lm(model, typ=2)
print("ANOVA de dos vías utilizando la fórmula de regresión")
print(anova_table)
# Reestructurar el DataFrame para que sea compatible con boxplot de seaborn
data_melted = pd.melt(df, id_vars=['COMBUSTIBLE'], value_vars=['CANTIDAD_CONSUMIDA', 'PRECIO_COMBUSTIBLE'], var_name='Variable', value_name='Valor')

# Crear un boxplot combinado utilizando seaborn
sns.boxplot(data=data_melted, x='Variable', y='Valor', hue='COMBUSTIBLE')

# Etiquetas de los ejes
plt.xlabel("Variable")
plt.ylabel("Valor")

# Mostrar el gráfico
plt.show()