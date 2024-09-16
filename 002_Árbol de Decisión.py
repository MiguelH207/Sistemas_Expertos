from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# Datos mejorados: [Nivel de Hambre (1-10), Tiempo Disponible (minutos)]
# Etiquetas: 0 = Comida rápida, 1 = Comida casera, 2 = Comida gourmet
X = [
    [9, 10], [8, 15], [10, 5],  # Comida rápida
    [5, 45], [6, 50], [4, 60],  # Comida casera
    [3, 120], [2, 150], [1, 180],  # Comida gourmet
    [7, 20], [3, 60], [8, 30], [1, 200], [4, 40]  # Más ejemplos
]
y = [0, 0, 0, 1, 1, 1, 2, 2, 2, 0, 1, 0, 2, 1]

# Crear el árbol de decisión
clf = DecisionTreeClassifier(max_depth=3)  # Limitar la profundidad del árbol
clf.fit(X, y)

# Nuevos ejemplos
new_data = [[7, 20], [3, 90], [2, 150], [9, 5]]  # Predicciones
predictions = clf.predict(new_data)

# Mostrar resultados
tipos_comida = ['Comida rápida', 'Comida casera', 'Comida gourmet']
for i, pred in enumerate(predictions):
    print(f"Recomendación para la instancia {i + 1}: {tipos_comida[pred]}")

# Visualizar el árbol
plt.figure(figsize=(10, 6))
plot_tree(clf, feature_names=['Hambre', 'Tiempo'], class_names=tipos_comida, filled=True, rounded=True)
plt.show()
