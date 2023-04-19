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

# Abrir el archivo JSON y cargar los datos en una variable de lista
with open('datos.json', 'r') as archivo:
    datos = json.load(archivo)

# Imprimir los datos en la consola
df = pd.DataFrame(datos)

# Realizar un ANOVA de una vía
modelo_anova = ols('TOTAL_CONSUMIDO ~ C(USUARIO_ASIGNACION)', data=df).fit()
tabla_anova = sm.stats.anova_lm(modelo_anova, typ=1)
print("Tabla ANOVA")
print(tabla_anova)

# Prueba post-hoc de Games-Howell (Tukey HSD como aproximación)
resultado_tukey = pairwise_tukeyhsd(df["TOTAL_CONSUMIDO"], df["USUARIO_ASIGNACION"], alpha=0.05)
print("\nPrueba post-hoc de Games-Howell (usando Tukey HSD como aproximación)")
print(resultado_tukey.summary())

# Gráfica de medidas de tendencia central, dispersión y forma
fig, ax = plt.subplots()

# Calcular medidas de tendencia central, dispersión y forma
media = df["TOTAL_CONSUMIDO"].mean()
mediana = df["TOTAL_CONSUMIDO"].median()
moda = df["TOTAL_CONSUMIDO"].mode()[0]
desviacion_estandar = np.std(df["TOTAL_CONSUMIDO"])
varianza = np.var(df["TOTAL_CONSUMIDO"])
asimetria = stats.skew(df["TOTAL_CONSUMIDO"])
curtosis = stats.kurtosis(df["TOTAL_CONSUMIDO"])
# Realizar la prueba post-hoc de Games-Howell
games_howell = pg.pairwise_gameshowell(data=df, dv="TOTAL_CONSUMIDO", between="USUARIO_ASIGNACION")

# Mostrar los resultados
print("Resultados de la prueba post-hoc de Games-Howell:")
print(games_howell)

# Mostrar información en la gráfica
sns.histplot(df, x="TOTAL_CONSUMIDO", kde=True, stat="density", ax=ax)
ax.axvline(media, color='r', linestyle='--', label=f'Media: {media:.2f}')
ax.axvline(mediana, color='g', linestyle='-', label=f'Mediana: {mediana:.2f}')
ax.axvline(moda, color='b', linestyle='-.', label=f'Moda: {moda:.2f}')
ax.legend()


plt.xlabel("TOTAL_CONSUMIDO")
plt.ylabel("Frecuencia relativa")
plt.title(f"Desviación estándar: {desviacion_estandar:.2f}, Varianza: {varianza:.2f}, Asimetría: {asimetria:.2f}, Curtosis: {curtosis:.2f}")
plt.show()
# Crear un boxplot agrupado por USUARIO_ASIGNACION para la columna TOTAL_CONSUMIDO
sns.boxplot(x="USUARIO_ASIGNACION", y="TOTAL_CONSUMIDO", data=df)

# Etiquetas de los ejes
plt.xlabel("USUARIO_ASIGNACION")
plt.ylabel("TOTAL_CONSUMIDO")

# Mostrar el gráfico
plt.show()


