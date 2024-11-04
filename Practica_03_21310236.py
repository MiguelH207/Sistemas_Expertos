import random
import pandas as pd
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import unidecode

# Cargar la base de datos y normalizar el texto
db_path = "base_datos_151_pokemon_con_generacion.csv"
df_pokemon = pd.read_csv(db_path)
# Definir la ruta de imágenes al inicio del código
ruta_imagenes = "imagenes_pokemon/"


# Normalizar la base de datos
def normalizar_texto(texto):
    return unidecode.unidecode(texto.strip().lower())

for columna in ["nombre", "tipo", "color", "forma", "nivel_evolucion"]:
    df_pokemon[columna] = df_pokemon[columna].apply(normalizar_texto)

pokemon_list = df_pokemon.to_dict(orient='records')

# Función para agregar un nuevo Pokémon con normalización en la entrada
def agregar_pokemon():
    def guardar_nuevo_pokemon():
        # Recoger y normalizar los valores de los campos de entrada
        nuevo_pokemon = pd.DataFrame([{
            "nombre": normalizar_texto(entry_nombre.get()).capitalize(),
            "tipo": normalizar_texto(entry_tipo.get()).capitalize(),
            "color": normalizar_texto(entry_color.get()).capitalize(),
            "forma": normalizar_texto(entry_forma.get()).capitalize(),
            "nivel_evolucion": entry_nivel.get().strip(),  # Ajustaremos después el valor a números
            "generacion": int(entry_generacion.get().strip()),
            "numero": int(entry_numero.get().strip())
        }])
        
        # Agregar el nuevo Pokémon al DataFrame y guardar en el archivo CSV
        global df_pokemon
        df_pokemon = pd.concat([df_pokemon, nuevo_pokemon], ignore_index=True)
        df_pokemon.to_csv(db_path, index=False)

        # Cerrar la ventana de agregar y regresar al menú principal
        ventana_agregar.destroy()
        
        # Notificación al usuario
        messagebox.showinfo("Nuevo Pokémon Agregado", 
                            "El nuevo Pokémon se ha agregado. "
                            "Recuerda incluir su imagen en la carpeta de imágenes.")
        
    # Ventana para ingresar los atributos del nuevo Pokémon
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar Pokémon")
    ventana_agregar.geometry("400x400")

    # Etiquetas y campos de entrada para cada atributo
    tk.Label(ventana_agregar, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana_agregar)
    entry_nombre.pack()

    tk.Label(ventana_agregar, text="Tipo").pack()
    entry_tipo = tk.Entry(ventana_agregar)
    entry_tipo.pack()

    tk.Label(ventana_agregar, text="Color").pack()
    entry_color = tk.Entry(ventana_agregar)
    entry_color.pack()

    tk.Label(ventana_agregar, text="Forma").pack()
    entry_forma = tk.Entry(ventana_agregar)
    entry_forma.pack()

    tk.Label(ventana_agregar, text="Nivel de Evolución").pack()
    entry_nivel = tk.Entry(ventana_agregar)
    entry_nivel.pack()

    tk.Label(ventana_agregar, text="Generación").pack()
    entry_generacion = tk.Entry(ventana_agregar)
    entry_generacion.pack()

    tk.Label(ventana_agregar, text="Número en Pokédex").pack()
    entry_numero = tk.Entry(ventana_agregar)
    entry_numero.pack()

    # Botón para guardar el nuevo Pokémon
    boton_guardar = tk.Button(ventana_agregar, text="Guardar Pokémon", command=guardar_nuevo_pokemon)
    boton_guardar.pack(pady=10)

# Función para actualizar la pregunta en la misma ventana
def actualizar_pregunta(atributo, valor):
    global pokemon_filtrados, atributos

    # Normalizar el valor de la pregunta
    valor_normalizado = normalizar_texto(valor)

    def respuesta_si():
        global pokemon_filtrados, atributos
        pokemon_filtrados = [p for p in pokemon_filtrados if normalizar_texto(p[atributo]) == valor_normalizado]
        atributos = [a for a in atributos if a[0] != atributo]
        siguiente_pregunta()

    def respuesta_no():
        global pokemon_filtrados
        pokemon_filtrados = [p for p in pokemon_filtrados if normalizar_texto(p[atributo]) != valor_normalizado]
        siguiente_pregunta()

    def respuesta_no_lo_se():
        siguiente_pregunta()

    pregunta_label.config(text=f"¿Tu Pokémon es {atributo} {valor}?")
    boton_si.config(command=respuesta_si)
    boton_no.config(command=respuesta_no)
    boton_no_lo_se.config(command=respuesta_no_lo_se)

# Función para iniciar el simulador de preguntas
def iniciar_preguntas():
    global pokemon_filtrados, atributos, pregunta_label, boton_si, boton_no, boton_no_lo_se

    pokemon_filtrados = pokemon_list.copy()
    atributos = [
        ("tipo", list(set([p["tipo"] for p in pokemon_filtrados]))),
        ("color", list(set([p["color"] for p in pokemon_filtrados]))),
        ("forma", list(set([p["forma"] for p in pokemon_filtrados]))),
        ("nivel_evolucion", list(set([p["nivel_evolucion"] for p in pokemon_filtrados]))),
        ("generacion", list(set([p["generacion"] for p in pokemon_filtrados])))
    ]

    global ventana_pregunta
    ventana_pregunta = tk.Toplevel(ventana)
    ventana_pregunta.title("Adivina Quién - Preguntas")
    ventana_pregunta.geometry("400x200")

    pregunta_label = tk.Label(ventana_pregunta, text="", font=("Arial", 12))
    pregunta_label.pack(pady=20)

    boton_si = tk.Button(ventana_pregunta, text="Sí", command=None, width=10)
    boton_si.pack(side="left", padx=10, pady=10)

    boton_no = tk.Button(ventana_pregunta, text="No", command=None, width=10)
    boton_no.pack(side="left", padx=10, pady=10)

    boton_no_lo_se = tk.Button(ventana_pregunta, text="No lo sé", command=None, width=10)
    boton_no_lo_se.pack(side="left", padx=10, pady=10)

    siguiente_pregunta()

# Función para mostrar la lista de Pokémon
def mostrar_lista_pokemon(iniciar_preguntas_callback):
    ventana_lista = tk.Toplevel(ventana)
    ventana_lista.title("Lista de Pokémon")
    ventana_lista.geometry("1200x600")

    frame_principal = tk.Frame(ventana_lista)
    frame_principal.pack(fill="both", expand=True)

    canvas = tk.Canvas(frame_principal)
    canvas.pack(side="left", fill="both", expand=True)

    scroll_y = tk.Scrollbar(frame_principal, orient="vertical", command=canvas.yview)
    scroll_y.pack(side="right", fill="y")

    scroll_x = tk.Scrollbar(ventana_lista, orient="horizontal", command=canvas.xview)
    scroll_x.pack(side="bottom", fill="x")

    marco_interior = tk.Frame(canvas)
    canvas.create_window((0, 0), window=marco_interior, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    for index, pokemon in enumerate(pokemon_list):
        frame_pokemon = tk.Frame(marco_interior, relief="solid", borderwidth=1)
        frame_pokemon.grid(row=index//15, column=index%15, padx=5, pady=5)

        nombre_archivo = f"{ruta_imagenes}{pokemon['numero']:0>3}.png"
        try:
            imagen = Image.open(nombre_archivo)
            imagen = imagen.resize((80, 80))
            imagen_tk = ImageTk.PhotoImage(imagen)
        except FileNotFoundError:
            imagen_tk = None

        if imagen_tk:
            etiqueta_imagen = tk.Label(frame_pokemon, image=imagen_tk)
            etiqueta_imagen.image = imagen_tk
            etiqueta_imagen.pack()
        else:
            etiqueta_placeholder = tk.Label(frame_pokemon, text="Img\nNo Disp.", font=("Arial", 8), width=6, height=3)
            etiqueta_placeholder.pack()

        etiqueta_nombre = tk.Label(frame_pokemon, text=pokemon["nombre"].capitalize(), font=("Arial", 8))
        etiqueta_nombre.pack()

    marco_interior.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    ventana_lista.wait_window()
    iniciar_preguntas_callback()

# Función para manejar las preguntas y avanzar
def siguiente_pregunta():
    global pokemon_filtrados, atributos

    if len(pokemon_filtrados) == 1:
        messagebox.showinfo("Resultado", f"¿Tu Pokémon es {pokemon_filtrados[0]['nombre'].capitalize()}?")
        ventana_pregunta.destroy()
        return

    if not atributos:
        messagebox.showinfo("Resultado", "No se pudo adivinar el Pokémon.")
        ventana_pregunta.destroy()
        return

    atributo, valores = atributos[0]
    if valores:
        valor = valores.pop(0)
        actualizar_pregunta(atributo, valor)
    else:
        atributos.pop(0)
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

# Crear la ventana principal con Tkinter
ventana = tk.Tk()
ventana.title("Adivina Quién - Pokémon")
ventana.geometry("300x250")

# Botón para jugar
boton_jugar = tk.Button(ventana, text="Jugar", command=iniciar_juego, width=10, height=2)
boton_jugar.pack(pady=10)

# Botón para agregar Pokémon
boton_agregar = tk.Button(ventana, text="Agregar Pokémon", command=agregar_pokemon, width=10, height=2)
boton_agregar.pack(pady=10)

# Botón para salir
boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy, width=10, height=2)
boton_salir.pack(pady=10)

# Iniciar la interfaz
ventana.mainloop()
