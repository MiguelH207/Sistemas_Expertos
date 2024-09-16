from sklearn.linear_model import LinearRegression
import numpy as np

# Datos mejorados: [Año]
X = np.array([[2015], [2016], [2017], [2018], [2019], [2020], [2021], [2022]])
# Precios en USD por galón
y = np.array([2.5, 2.6, 2.7, 2.8, 3.0, 2.9, 3.1, 3.2])

# Crear el modelo de regresión lineal
reg = LinearRegression()
reg.fit(X, y)

# Predicción para el año 2023
precio_2023 = reg.predict([[2023]])
print(f"Predicción del precio de la gasolina en 2023: ${precio_2023[0]:.2f} por galón")
