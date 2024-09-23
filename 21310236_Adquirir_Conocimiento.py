import json
import os

# Archivo donde se almacenará la base de conocimiento
archivo_base_conocimiento = 'base_conocimiento.json'

# Función para cargar la base de conocimiento desde el archivo JSON
def cargar_base_conocimiento():
    if os.path.exists(archivo_base_conocimiento):
        with open(archivo_base_conocimiento, 'r') as file:
            return json.load(file)
    else:
        # Si el archivo no existe, inicializamos con una base de conocimiento predeterminada
        return {
            "hola": "¡Hola! ¿Cómo estás?",
            "como estas": "Estoy bien, gracias. ¿Y tú?",
            "de que te gustaria hablar": "Me gustaría hablar sobre cualquier tecnología, como inteligencia artificial, redes neuronales o blockchain."
        }

# Función para guardar la base de conocimiento en un archivo JSON
def guardar_base_conocimiento(base_conocimiento):
    with open(archivo_base_conocimiento, 'w') as file:
        json.dump(base_conocimiento, file, indent=4)

# Función para gestionar las preguntas del usuario
def preguntar_usuario(pregunta, base_conocimiento):
    pregunta = pregunta.lower()
    
    # Verificar si la pregunta está en la base de conocimiento
    if pregunta in base_conocimiento:
        return base_conocimiento[pregunta]
    else:
        # Si no está, pedir al usuario la respuesta
        nueva_respuesta = input(f"No tengo una respuesta para '{pregunta}'. ¿Cuál debería ser la respuesta?: ")
        # Agregar la nueva pregunta y respuesta a la base de conocimiento
        base_conocimiento[pregunta] = nueva_respuesta
        # Guardar la base de conocimiento actualizada
        guardar_base_conocimiento(base_conocimiento)
        return f"¡Gracias! Ahora sé la respuesta a '{pregunta}'."

# Función principal para el chat
def chat():
    print("¡Bienvenido al chat tecnológico! Escribe 'salir' para terminar la conversación.")
    
    # Cargar la base de conocimiento desde el archivo JSON
    base_conocimiento = cargar_base_conocimiento()
    
    while True:
        # Obtener la entrada del usuario
        pregunta_usuario = input("\nTú: ")
        if pregunta_usuario.lower() == "salir":
            print("¡Hasta luego!")
            break
        # Obtener la respuesta usando la función preguntar_usuario
        respuesta = preguntar_usuario(pregunta_usuario, base_conocimiento)
        print(f"Chatbot: {respuesta}")

# Iniciar el chat
chat()
