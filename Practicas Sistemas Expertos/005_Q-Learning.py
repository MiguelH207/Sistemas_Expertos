import numpy as np

# Definir el entorno de la ciudad como una matriz de recompensas
# -1 = No hay conexión, 0 = Movimientos permitidos, 100 = Destino final (recompensa máxima)
recompensas = np.array([
    [-1, -1, -1, -1, 0, -1],
    [-1, -1, -1, 0, -1, 100],
    [-1, -1, -1, 0, -1, -1],
    [-1, 0, 0, -1, 0, -1],
    [0, -1, -1, 0, -1, 100],
    [-1, 0, -1, -1, 0, 100]
])

# Inicializar la matriz Q
Q = np.zeros_like(recompensas)

# Parámetros de Q-Learning
gamma = 0.8  # Factor de descuento
alpha = 0.9  # Tasa de aprendizaje
episodios = 1000  # Número de episodios

# Función de aprendizaje de Q-Learning
def aprender_Q():
    for _ in range(episodios):
        estado = np.random.randint(0, 6)  # Estado inicial aleatorio

        while estado != 5:  # Estado 5 es el destino final (meta)
            # Seleccionar una acción válida (movimiento posible)
            acciones_validas = np.where(recompensas[estado] >= 0)[0]
            accion = np.random.choice(acciones_validas)

            # Actualizar el valor de Q según la fórmula de Q-learning
            Q[estado, accion] = Q[estado, accion] + alpha * (
                recompensas[estado, accion] + gamma * np.max(Q[accion]) - Q[estado, accion]
            )

            # Mover al siguiente estado
            estado = accion

# Aprender la política óptima
aprender_Q()

# Mostrar la matriz Q después del aprendizaje
print("Matriz Q después del aprendizaje:")
print(Q)

# Probar la ruta óptima desde un estado inicial (por ejemplo, estado 2)
estado_inicial = 2
ruta = [estado_inicial]

while estado_inicial != 5:
    siguiente_estado = np.argmax(Q[estado_inicial])
    ruta.append(siguiente_estado)
    estado_inicial = siguiente_estado

print(f"Ruta óptima desde el estado inicial: {ruta}")
