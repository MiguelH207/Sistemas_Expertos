import tkinter as tk
from tkinter import messagebox
import random

# Definir personajes con características mejoradas para asegurar la adivinanza
personajes = [
    {"nombre": "Jett", "rol": "duelista", "habilidad": "movilidad", "nacionalidad": "Coreana", "arma": "cuchillo", "color_cabello": "blanco"},
    {"nombre": "Phoenix", "rol": "duelista", "habilidad": "control de fuego", "nacionalidad": "Británico", "arma": "pistola", "color_cabello": "oscuro"},
    {"nombre": "Raze", "rol": "duelista", "habilidad": "explosiva", "nacionalidad": "Brasileño", "arma": "lanzagranadas", "color_cabello": "naranja"},
    {"nombre": "Reyna", "rol": "duelista", "habilidad": "absorción de almas", "nacionalidad": "Mexicano", "arma": "pistola", "color_cabello": "morado"},
    {"nombre": "Yoru", "rol": "duelista", "habilidad": "teletransportación", "nacionalidad": "Japonés", "arma": "cuchillo", "color_cabello": "azul"},
    {"nombre": "Brimstone", "rol": "controlador", "habilidad": "bombardeo", "nacionalidad": "Americano", "arma": "rifle", "color_cabello": "canoso"},
    {"nombre": "Omen", "rol": "controlador", "habilidad": "control de sombras", "nacionalidad": "desconocido", "arma": "espada", "color_cabello": "negro"},
    {"nombre": "Viper", "rol": "controlador", "habilidad": "veneno", "nacionalidad": "Americano", "arma": "rifle", "color_cabello": "verde"},
    {"nombre": "Astra", "rol": "controlador", "habilidad": "control de estrellas", "nacionalidad": "Ghanés", "arma": "rifle", "color_cabello": "violeta"},
    {"nombre": "Harbor", "rol": "controlador", "habilidad": "control de agua", "nacionalidad": "Indio", "arma": "rifle", "color_cabello": "oscuro"},
    {"nombre": "Sova", "rol": "iniciador", "habilidad": "detección", "nacionalidad": "Ruso", "arma": "arco", "color_cabello": "rubio"},
    {"nombre": "Skye", "rol": "iniciador", "habilidad": "curación", "nacionalidad": "Australiano", "arma": "rifle", "color_cabello": "rubio"},
    {"nombre": "Breach", "rol": "iniciador", "habilidad": "terremotos", "nacionalidad": "Sueco", "arma": "rifle", "color_cabello": "naranja"},
    {"nombre": "KAY/O", "rol": "iniciador", "habilidad": "supresión", "nacionalidad": "robot", "arma": "granada", "color_cabello": "metálico"},
    {"nombre": "Gekko", "rol": "iniciador", "habilidad": "invocación", "nacionalidad": "Mexicano", "arma": "pistola", "color_cabello": "verde"},
    {"nombre": "Sage", "rol": "centinela", "habilidad": "curación", "nacionalidad": "Chino", "arma": "pistola", "color_cabello": "negro"},
    {"nombre": "Killjoy", "rol": "centinela", "habilidad": "tecnología", "nacionalidad": "Alemán", "arma": "torreta", "color_cabello": "amarillo"},
    {"nombre": "Cypher", "rol": "centinela", "habilidad": "trampas", "nacionalidad": "Marroquí", "arma": "trampa", "color_cabello": "oscuro"},
    {"nombre": "Chamber", "rol": "centinela", "habilidad": "teletransportación", "nacionalidad": "Francés", "arma": "pistola", "color_cabello": "rubio"},
    {"nombre": "Neon", "rol": "duelista", "habilidad": "electricidad", "nacionalidad": "Filipino", "arma": "rifle", "color_cabello": "azul"},
    {"nombre": "Fade", "rol": "iniciador", "habilidad": "pesadillas", "nacionalidad": "Turco", "arma": "pistola", "color_cabello": "negro"},
    {"nombre": "Deadlock", "rol": "centinela", "habilidad": "control de masas", "nacionalidad": "Noruego", "arma": "rifle", "color_cabello": "gris"},
    {"nombre": "Harbinger", "rol": "controlador", "habilidad": "control de tierra", "nacionalidad": "Indio", "arma": "martillo", "color_cabello": "negro"},
    {"nombre": "Raijin", "rol": "duelista", "habilidad": "control de viento", "nacionalidad": "Coreano", "arma": "espada", "color_cabello": "blanco"},
    {"nombre": "Glitch", "rol": "iniciador", "habilidad": "interferencia", "nacionalidad": "Japonés", "arma": "hacha", "color_cabello": "rosa"}
]

# Preguntas genéricas
preguntas_genericas = [
    {"pregunta": "¿El personaje es un duelista?", "atributo": "rol", "valor": "duelista"},
    {"pregunta": "¿El personaje es un controlador?", "atributo": "rol", "valor": "controlador"},
    {"pregunta": "¿El personaje es un iniciador?", "atributo": "rol", "valor": "iniciador"},
    {"pregunta": "¿El personaje es un centinela?", "atributo": "rol", "valor": "centinela"},
    {"pregunta": "¿El personaje tiene habilidades ofensivas?", "atributo": "habilidad", "valor": "ofensiva"},
    {"pregunta": "¿El personaje tiene habilidades defensivas?", "atributo": "habilidad", "valor": "defensiva"}
]

# Preguntas específicas
preguntas_especificas = [
    {"pregunta": "¿El personaje es de nacionalidad rusa?", "atributo": "nacionalidad", "valor": "Ruso"},
    {"pregunta": "¿El personaje tiene el cabello blanco?", "atributo": "color_cabello", "valor": "blanco"},
    {"pregunta": "¿El personaje tiene habilidades de control de fuego?", "atributo": "habilidad", "valor": "control de fuego"},
    {"pregunta": "¿El personaje tiene habilidades de teletransportación?", "atributo": "habilidad", "valor": "teletransportación"},
    {"pregunta": "¿El personaje tiene habilidades de curación?", "atributo": "habilidad", "valor": "curación"},
    {"pregunta": "¿El personaje tiene habilidades de veneno?", "atributo": "habilidad", "valor": "veneno"},
    {"pregunta": "¿El personaje tiene habilidades explosivas?", "atributo": "habilidad", "valor": "explosiva"},
    {"pregunta": "¿El personaje es de nacionalidad mexicana?", "atributo": "nacionalidad", "valor": "Mexicano"},
    {"pregunta": "¿El personaje es de nacionalidad japonesa?", "atributo": "nacionalidad", "valor": "Japonés"},
    {"pregunta": "¿El personaje usa cuchillos como arma?", "atributo": "arma", "valor": "cuchillo"},
    {"pregunta": "¿El personaje tiene el cabello azul?", "atributo": "color_cabello", "valor": "azul"},
    {"pregunta": "¿El personaje usa un arco?", "atributo": "arma", "valor": "arco"},
    {"pregunta": "¿El personaje tiene habilidades de control de estrellas?", "atributo": "habilidad", "valor": "control de estrellas"},
    {"pregunta": "¿El personaje tiene habilidades de supresión?", "atributo": "habilidad", "valor": "supresión"},
    {"pregunta": "¿El personaje tiene habilidades de electricidad?", "atributo": "habilidad", "valor": "electricidad"}
]

class AdivinaQuienApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina Quién: Valorant Edition")
        self.root.geometry("500x400")

        # Copia de la lista de personajes
        self.personajes_restantes = personajes.copy()
        self.pregunta_actual = None
        self.puntuacion = 0
        self.preguntas_realizadas = 0
        self.min_preguntas_genericas = 3
        self.uso_preguntas_genericas = True

        # Configuración de la interfaz
        self.lbl_instruccion = tk.Label(root, text="Piensa en un personaje de Valorant...", font=("Arial", 14))
        self.lbl_instruccion.pack(pady=20)

        self.btn_iniciar = tk.Button(root, text="Iniciar Juego", command=self.iniciar_juego, font=("Arial", 12))
        self.btn_iniciar.pack(pady=10)

        self.lbl_pregunta = tk.Label(root, text="", font=("Arial", 12))
        self.lbl_pregunta.pack(pady=10)

        self.btn_si = tk.Button(root, text="Sí", command=lambda: self.responder("sí"), state="disabled", width=10)
        self.btn_si.pack(side="left", padx=20)

        self.btn_no = tk.Button(root, text="No", command=lambda: self.responder("no"), state="disabled", width=10)
        self.btn_no.pack(side="left", padx=20)

    def iniciar_juego(self):
        self.btn_iniciar.config(state="disabled")
        self.btn_si.config(state="normal")
        self.btn_no.config(state="normal")
        self.puntuacion = 0
        self.preguntas_realizadas = 0
        self.uso_preguntas_genericas = True
        self.hacer_pregunta()

    def hacer_pregunta(self):
        if self.preguntas_realizadas >= self.min_preguntas_genericas:
            self.uso_preguntas_genericas = False

        if self.uso_preguntas_genericas:
            self.pregunta_actual = random.choice(preguntas_genericas)
        else:
            if len(self.personajes_restantes) == 1:
                self.adivinar_personaje()
                return
            self.pregunta_actual = random.choice(preguntas_especificas)

        self.lbl_pregunta.config(text=self.pregunta_actual["pregunta"])
        self.preguntas_realizadas += 1
        self.puntuacion += 1

    def responder(self, respuesta):
        if respuesta == "sí":
            self.personajes_restantes = [p for p in self.personajes_restantes 
                                         if p[self.pregunta_actual["atributo"]] == self.pregunta_actual["valor"]]
        else:
            self.personajes_restantes = [p for p in self.personajes_restantes 
                                         if p[self.pregunta_actual["atributo"]] != self.pregunta_actual["valor"]]

        if not self.personajes_restantes:
            messagebox.showinfo("Adivina Quién", "No pude adivinar tu personaje. ¡Intenta de nuevo!")
            self.reiniciar_juego()
        else:
            self.hacer_pregunta()

    def adivinar_personaje(self):
        personaje_adivinado = self.personajes_restantes[0]
        messagebox.showinfo("Adivina Quién", f"¡Tu personaje es {personaje_adivinado['nombre']}!\nPuntuación: {self.puntuacion}")
        self.reiniciar_juego()

    def reiniciar_juego(self):
        self.personajes_restantes = personajes.copy()
        self.pregunta_actual = None
        self.lbl_pregunta.config(text="")
        self.btn_iniciar.config(state="normal")
        self.btn_si.config(state="disabled")
        self.btn_no.config(state="disabled")

# Ejecutar la aplicación
root = tk.Tk()
app = AdivinaQuienApp(root)
root.mainloop()
