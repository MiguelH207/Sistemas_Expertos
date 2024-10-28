import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Cargar la base de datos desde un archivo CSV
df_pokemon = pd.read_csv("base_datos_151_pokemon.csv")
pokemon_list = df_pokemon.to_dict(orient='records')

# Ruta del directorio de imágenes (ajústala a tu directorio real)
ruta_imagenes = "imagenes_pokemon/"

# Función para mostrar la ventana con las imágenes y nombres de los Pokémon
def mostrar_lista_pokemon(iniciar_preguntas_callback):
    ventana_lista = tk.Toplevel(ventana)
    ventana_lista.title("Lista de Pokémon")
    ventana_lista.geometry("1200x600")  # Ajustar ancho de la ventana

    # Crear un marco principal con un canvas para el scrolleo
    frame_principal = tk.Frame(ventana_lista)
    frame_principal.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_principal)
    canvas.pack(side="left", fill="both", expand=True)

    # Crear barras de desplazamiento
    scroll_y = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(ventana_lista, orient="horizontal", command=canvas.xview)
    scroll_x.pack(side="bottom", fill="x")

    # Crear un marco interior para el contenido
    marco_interior = tk.Frame(canvas)

    # Configurar el canvas
    canvas.create_window((0, 0), window=marco_interior, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    # Mostrar los Pokémon en una cuadrícula de 15 por fila
    for index, pokemon in enumerate(pokemon_list):
        frame_pokemon = tk.Frame(marco_interior, relief="solid", borderwidth=1)
        frame_pokemon.grid(row=index//15, column=index%15, padx=5, pady=5)

        # Cargar la imagen del Pokémon usando el número de la Pokédex con tres dígitos
        nombre_archivo = f"{ruta_imagenes}{pokemon['numero']:0>3}.png"
        try:
            imagen = Image.open(nombre_archivo)
            imagen = imagen.resize((80, 80))  # Ajustar el tamaño de la imagen
            imagen_tk = ImageTk.PhotoImage(imagen)
        except FileNotFoundError:
            imagen_tk = None

        # Mostrar la imagen si se cargó correctamente
        if imagen_tk:
            etiqueta_imagen = tk.Label(frame_pokemon, image=imagen_tk)
            etiqueta_imagen.image = imagen_tk
            etiqueta_imagen.pack()
        else:
            etiqueta_placeholder = tk.Label(frame_pokemon, text="Img\nNo Disp.", font=("Arial", 8), width=6, height=3)
            etiqueta_placeholder.pack()

        etiqueta_nombre = tk.Label(frame_pokemon, text=pokemon["nombre"], font=("Arial", 8))
        etiqueta_nombre.pack()

    # Configurar el tamaño del marco interior para el scrolleo
    marco_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # Esperar a que se cierre la ventana de la lista antes de iniciar las preguntas
    ventana_lista.wait_window()

    # Iniciar las preguntas después de cerrar la ventana de la lista
    iniciar_preguntas_callback()

# Función para manejar las preguntas y avanzar
def siguiente_pregunta():
    global pokemon_filtrados, atributos

    if len(pokemon_filtrados) == 1:
        messagebox.showinfo("Resultado", f"¿Tu Pokémon es {pokemon_filtrados[0]['nombre']}?")
        ventana_pregunta.destroy()
        return

    if not atributos:
        messagebox.showinfo("Resultado", "No se pudo adivinar el Pokémon.")
        ventana_pregunta.destroy()
        return

    # Obtener el siguiente atributo y valor
    atributo, valores = atributos[0]
    if valores:
        valor = valores.pop(0)
        actualizar_pregunta(atributo, valor)
    else:
        atributos.pop(0)
        siguiente_pregunta()

# Función para actualizar la pregunta en la misma ventana
def actualizar_pregunta(atributo, valor):
    global pokemon_filtrados, atributos

    def respuesta_si():
        global pokemon_filtrados, atributos
        pokemon_filtrados = [p for p in pokemon_filtrados if p[atributo] == valor]
        atributos = [a for a in atributos if a[0] != atributo]
        siguiente_pregunta()

    def respuesta_no():
        global pokemon_filtrados
        pokemon_filtrados = [p for p in pokemon_filtrados if p[atributo] != valor]
        siguiente_pregunta()

    def respuesta_no_lo_se():
        siguiente_pregunta()

    pregunta_label.config(text=f"¿Tu Pokémon tiene {atributo} {valor}?")
    boton_si.config(command=respuesta_si)
    boton_no.config(command=respuesta_no)
    boton_no_lo_se.config(command=respuesta_no_lo_se)

# Función para iniciar el simulador de preguntas
def iniciar_preguntas():
    global pokemon_filtrados, atributos, pregunta_label, boton_si, boton_no, boton_no_lo_se

    pokemon_filtrados = pokemon_list.copy()  # Copiar la lista original de Pokémon
    atributos = [
        ("tipo", list(set([p["tipo"] for p in pokemon_filtrados]))),
        ("color", list(set([p["color"] for p in pokemon_filtrados]))),
        ("forma", list(set([p["forma"] for p in pokemon_filtrados]))),
        ("tamaño", list(set([p["tamaño"] for p in pokemon_filtrados])))
    ]

    global ventana_pregunta
    ventana_pregunta = tk.Toplevel(ventana)
    ventana_pregunta.title("Adivina Quién - Preguntas")
    ventana_pregunta.geometry("400x200")

    pregunta_label = tk.Label(ventana_pregunta, text="", font=("Arial", 12))
    pregunta_label.pack(pady=20)

    # Botones para las respuestas
    boton_si = tk.Button(ventana_pregunta, text="Sí", command=None, width=10)
    boton_si.pack(side="left", padx=10, pady=10)

    boton_no = tk.Button(ventana_pregunta, text="No", command=None, width=10)
    boton_no.pack(side="left", padx=10, pady=10)

    boton_no_lo_se = tk.Button(ventana_pregunta, text="No lo sé", command=None, width=10)
    boton_no_lo_se.pack(side="left", padx=10, pady=10)

    siguiente_pregunta()

# Función para iniciar el juego completo
def iniciar_juego():
    def mostrar_explicacion():
        ventana_explicacion = tk.Toplevel(ventana)
        ventana_explicacion.title("Explicación")
        ventana_explicacion.geometry("400x200")

        etiqueta_explicacion = tk.Label(ventana_explicacion, 
                                        text="Piensa en un Pokémon y responde a las preguntas con 'Sí', 'No', o 'No lo sé'.")
        etiqueta_explicacion.pack(pady=20)

        boton_continuar = tk.Button(ventana_explicacion, text="Continuar", 
                                    command=lambda: [ventana_explicacion.destroy(), mostrar_opcion_ver_lista()])
        boton_continuar.pack(pady=20)

    def mostrar_opcion_ver_lista():
        ventana_opcion = tk.Toplevel(ventana)
        ventana_opcion.title("¿Ver lista de Pokémon?")
        ventana_opcion.geometry("400x200")

        etiqueta_opcion = tk.Label(ventana_opcion, text="¿Quieres ver la lista de Pokémon disponibles?", font=("Arial", 12))
        etiqueta_opcion.pack(pady=20)

        boton_si = tk.Button(ventana_opcion, text="Sí", 
                             command=lambda: [ventana_opcion.destroy(), mostrar_lista_pokemon(iniciar_preguntas)])
        boton_si.pack(side="left", padx=10, pady=20)

        boton_no = tk.Button(ventana_opcion, text="No", 
                             command=lambda: [ventana_opcion.destroy(), iniciar_preguntas()])
        boton_no.pack(side="right", padx=10, pady=20)

    mostrar_explicacion()

# Función para salir del juego
def salir():
    ventana.destroy()

# Crear la ventana principal con Tkinter
ventana = tk.Tk()
ventana.title("Adivina Quién - Pokémon")
ventana.geometry("300x200")

# Botón para jugar
boton_jugar = tk.Button(ventana, text="Jugar", command=iniciar_juego, width=10, height=2)
boton_jugar.pack(pady=20)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", command=salir, width=10, height=2)
boton_salir.pack(pady=10)

# Iniciar la interfaz
ventana.mainloop()
