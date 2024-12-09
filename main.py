import json
import tkinter as tk
from tkinter import messagebox

def cargar_datos_desde_json(ruta):
    """Carga los datos de la base de conocimientos desde un archivo JSON."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def calcular_diagnosticos(respuestas, posibles_sintomas):
    """Calcula los porcentajes de probabilidad para cada diagnóstico."""
    resultados = []
    for diagnostico, sintomas in posibles_sintomas.items():
        sintomas_confirmados = [sintoma for sintoma in sintomas if respuestas.get(sintoma) == 'si']
        sintomas_no_se = [sintoma for sintoma in sintomas if respuestas.get(sintoma) == 'no sé']
        sintomas_totales = len(sintomas)
        otros_sintomas = [sintoma for sintoma, respuesta in respuestas.items() if respuesta == 'si' and sintoma not in sintomas]

        if sintomas_totales > 0:
            porcentaje = (len(sintomas_confirmados) / sintomas_totales) * 100
            if otros_sintomas:
                penalizacion_ajenos = len(otros_sintomas) * 5
                porcentaje -= penalizacion_ajenos
            if sintomas_no_se:
                penalizacion_no_se = (len(sintomas_no_se) / sintomas_totales) * 10
                porcentaje -= penalizacion_no_se
            porcentaje = max(0, porcentaje)
            resultados.append((diagnostico, porcentaje))
    return sorted(resultados, key=lambda x: x[1], reverse=True)

class SistemaExpertoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Experto: Diagnóstico de Fallas CNC")

        self.datos = cargar_datos_desde_json('base_conocimientos.json')
        self.posibles_sintomas = self.datos['posibles_sintomas']
        self.respuestas = {}
        self.preguntas = self.generar_preguntas()
        self.indice_pregunta = 0

        self.label_pregunta = tk.Label(master, text="", wraplength=400, font=("Arial", 12))
        self.label_pregunta.pack(pady=20)

        self.frame_botones = tk.Frame(master)
        self.frame_botones.pack(pady=10)

        self.boton_si = tk.Button(self.frame_botones, text="Sí", command=lambda: self.guardar_respuesta("si"))
        self.boton_si.pack(side="left", padx=10)

        self.boton_no = tk.Button(self.frame_botones, text="No", command=lambda: self.guardar_respuesta("no"))
        self.boton_no.pack(side="left", padx=10)

        self.boton_no_se = tk.Button(self.frame_botones, text="No sé", command=lambda: self.guardar_respuesta("no sé"))
        self.boton_no_se.pack(side="left", padx=10)

        self.mostrar_pregunta()

    def generar_preguntas(self):
        """Genera una lista de preguntas únicas basadas en los síntomas."""
        preguntas = []
        for sintomas in self.posibles_sintomas.values():
            preguntas.extend(sintomas)
        return list(set(preguntas))  # Elimina duplicados

    def mostrar_pregunta(self):
        """Muestra la pregunta actual en la interfaz."""
        if self.indice_pregunta < len(self.preguntas):
            self.label_pregunta.config(text=f"¿Presenta el síntoma: {self.preguntas[self.indice_pregunta]}?")
        else:
            self.mostrar_resultados()

    def guardar_respuesta(self, respuesta):
        """Guarda la respuesta para la pregunta actual."""
        sintoma = self.preguntas[self.indice_pregunta]
        self.respuestas[sintoma] = respuesta
        self.indice_pregunta += 1
        self.mostrar_pregunta()

    def mostrar_resultados(self):
        """Calcula y muestra los resultados finales en un mensaje emergente."""
        resultados = calcular_diagnosticos(self.respuestas, self.posibles_sintomas)
        mensaje = "Diagnósticos finales con porcentaje de probabilidad:\n\n"
        for diagnostico, porcentaje in resultados:
            mensaje += f"- {diagnostico}: {porcentaje:.2f}%\n"
        messagebox.showinfo("Resultados", mensaje)
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaExpertoGUI(root)
    root.mainloop()