from sklearn.naive_bayes import MultinomialNB

# Datos mejorados: [Ofertas, Descuentos, Urgente, Premio, Publicidad]
# Etiquetas: 0 = No spam, 1 = Spam
X = [
    [1, 1, 1, 0, 1], [1, 0, 0, 1, 1], [0, 1, 1, 1, 1],  # Spam
    [0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [1, 0, 0, 0, 0],  # No spam
    [0, 0, 1, 0, 1], [1, 1, 0, 1, 0], [0, 0, 0, 1, 1]  # Nuevos ejemplos
]
y = [1, 1, 1, 0, 0, 0, 0, 1, 1]

# Crear el modelo Naive Bayes
nb = MultinomialNB()
nb.fit(X, y)

# Nuevos correos para clasificar
new_emails = [[1, 1, 0, 0, 1], [0, 0, 1, 0, 0], [1, 0, 1, 1, 0]]
predictions = nb.predict(new_emails)

# Mostrar resultados
etiquetas = ['No spam', 'Spam']
for i, pred in enumerate(predictions):
    print(f"Clasificación para el correo {i + 1}: {etiquetas[pred]}")
