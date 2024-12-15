import json
import tkinter as tk
from tkinter import messagebox, simpledialog, PhotoImage

def cargar_datos_desde_json(ruta):
    """Carga los datos de la base de conocimientos desde un archivo JSON."""
    with open(ruta, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

def guardar_datos_a_json(ruta, datos):
    """Guarda los datos actualizados en el archivo JSON."""
    with open(ruta, 'w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

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

class MenuPrincipal:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema Experto CNC")
        self.master.geometry("600x400")

        # Título
        self.label_titulo = tk.Label(master, text="Sistema Experto: Diagnóstico de Fallas CNC", font=("Arial", 16), pady=20)
        self.label_titulo.pack()

        # Botones del menú
        self.boton_diagnostico = tk.Button(master, text="Realizar Diagnóstico", width=25, command=self.iniciar_diagnostico)
        self.boton_diagnostico.pack(pady=10)

        self.boton_administrar = tk.Button(master, text="Administrar Base de Datos", width=25, command=self.administrar)
        self.boton_administrar.pack(pady=10)

        self.boton_salir = tk.Button(master, text="Salir", width=25, command=master.quit)
        self.boton_salir.pack(pady=10)

    def iniciar_diagnostico(self):
        self.master.destroy()
        root = tk.Tk()
        SistemaExpertoGUI(root, regresar_menu=True)
        root.mainloop()

    def administrar(self):
        password = simpledialog.askstring("Contraseña", "Ingrese la contraseña para acceder:", show='*')
        if password == "admin":
            self.master.destroy()
            root = tk.Tk()
            AdministrarBaseDeDatos(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Contraseña incorrecta.")

class SistemaExpertoGUI:
    def __init__(self, master, regresar_menu=False):
        self.master = master
        self.master.title("Sistema Experto: Diagnóstico de Fallas CNC")
        self.master.geometry("600x400")  # Fijar tamaño de la ventana

        self.datos = cargar_datos_desde_json('base_conocimientos.json')
        self.posibles_sintomas = self.datos['posibles_sintomas']
        self.soluciones = self.datos['soluciones']
        self.respuestas = {}
        self.preguntas = self.generar_preguntas()
        self.indice_pregunta = 0
        self.regresar_menu = regresar_menu

        self.frame_contenido = tk.Frame(master, bg="white", bd=5, relief="raised")
        self.frame_contenido.place(relx=0.5, rely=0.5, anchor="center", width=500, height=250)

        self.label_pregunta = tk.Label(self.frame_contenido, text="", wraplength=480, font=("Arial", 12), bg="white")
        self.label_pregunta.pack(pady=20)

        self.frame_botones = tk.Frame(self.frame_contenido, bg="white")
        self.frame_botones.pack(pady=10)

        self.boton_si = tk.Button(self.frame_botones, text="Sí", width=10, command=lambda: self.guardar_respuesta("si"))
        self.boton_si.pack(side="left", padx=10)

        self.boton_no = tk.Button(self.frame_botones, text="No", width=10, command=lambda: self.guardar_respuesta("no"))
        self.boton_no.pack(side="left", padx=10)

        self.boton_no_se = tk.Button(self.frame_botones, text="No sé", width=10, command=lambda: self.guardar_respuesta("no sé"))
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
        """Calcula y muestra los resultados finales con soluciones propuestas."""
        resultados = calcular_diagnosticos(self.respuestas, self.posibles_sintomas)
        mensaje = "Diagnósticos finales con porcentaje de probabilidad:\n\n"
        for diagnostico, porcentaje in resultados:
            mensaje += f"- {diagnostico}: {porcentaje:.2f}%\n"
            if porcentaje > 0:
                mensaje += f"  Solución: {self.soluciones.get(diagnostico, 'No hay solución registrada.')}\n\n"

        if not resultados:
            mensaje = "No se encontraron fallas con suficiente probabilidad."

        messagebox.showinfo("Resultados", mensaje)

        if self.regresar_menu:
            self.master.destroy()
            root = tk.Tk()
            MenuPrincipal(root)
            root.mainloop()

    def reiniciar_diagnostico(self):
        """Reinicia el diagnóstico desde el inicio."""
        self.respuestas = {}
        self.preguntas = self.generar_preguntas()
        self.indice_pregunta = 0
        self.mostrar_pregunta()

class AdministrarBaseDeDatos:
    def __init__(self, master):
        self.master = master
        self.master.title("Administrar Base de Conocimientos")
        self.master.geometry("600x400")

        self.datos = cargar_datos_desde_json('base_conocimientos.json')

        self.label_titulo = tk.Label(master, text="Administrar Base de Datos", font=("Arial", 16), pady=20)
        self.label_titulo.pack()

        self.boton_agregar = tk.Button(master, text="Agregar Falla", width=25, command=self.agregar_falla)
        self.boton_agregar.pack(pady=10)

        self.boton_eliminar = tk.Button(master, text="Eliminar Falla", width=25, command=self.eliminar_falla)
        self.boton_eliminar.pack(pady=10)

        self.boton_volver = tk.Button(master, text="Volver al Menú Principal", width=25, command=self.volver_menu)
        self.boton_volver.pack(pady=10)

    def agregar_falla(self):
        nueva_falla = simpledialog.askstring("Nueva Falla", "Ingrese el nombre de la nueva falla:")
        if nueva_falla:
            nueva_solucion = simpledialog.askstring("Solución", f"Ingrese la solución para {nueva_falla}:")
            nueva_solucion = nueva_solucion if nueva_solucion else "No hay solución registrada."

            sintomas = []
            while True:
                sintoma = simpledialog.askstring("Nuevo Síntoma", "Ingrese un síntoma asociado o deje vacío para terminar:")
                if not sintoma:
                    break
                sintomas.append(sintoma)

            self.datos['posibles_sintomas'][nueva_falla] = sintomas
            self.datos['soluciones'][nueva_falla] = nueva_solucion
            guardar_datos_a_json('base_conocimientos.json', self.datos)
            messagebox.showinfo("Éxito", "Falla y sus síntomas agregados correctamente.")

    def eliminar_falla(self):
        falla = simpledialog.askstring("Eliminar Falla", "Ingrese el nombre de la falla a eliminar:")
        if falla in self.datos['posibles_sintomas']:
            del self.datos['posibles_sintomas'][falla]
            del self.datos['soluciones'][falla]
            guardar_datos_a_json('base_conocimientos.json', self.datos)
            messagebox.showinfo("Éxito", "Falla eliminada correctamente.")
        else:
            messagebox.showerror("Error", "La falla no existe.")

    def volver_menu(self):
        self.master.destroy()
        root = tk.Tk()
        MenuPrincipal(root)
        root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    MenuPrincipal(root)
    root.mainloop()
