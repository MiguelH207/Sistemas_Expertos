from rules import evaluate_facts

def main():
    print("\n=== Sistema Experto: Diagnóstico de Fallas CNC ===")

    # Obtener síntomas mediante preguntas de sí, no o no sé
    respuestas = {}  # Diccionario para almacenar las respuestas del usuario a cada síntoma.
    posibles_sintomas = {  # Diccionario con los diagnósticos y sus respectivos síntomas asociados.
        "vibraciones excesivas": ["ruido anormal", "vibraciones detectadas por sensores", "incremento en la desviación del corte"],
        "desalineación del eje": ["movimiento no lineal", "errores en la precisión de cortes", "ruido mecánico anormal"],
        "error en el control del eje": ["movimiento irregular", "ejes que no regresan a la posición inicial correctamente", "recalibración fallida"],
        "falla en el sistema de enfriamiento": ["sobrecalentamiento del cabezal", "baja presión del refrigerante", "fugas visibles en las tuberías"],
        "falla en el motor principal": ["ruido eléctrico", "variaciones en la velocidad", "paradas repentinas durante la operación"],
        "problema en el plc": ["pérdida de conexión", "sistema no responde a comandos", "alarmas de comunicación"],
        "herramientas desgastadas": ["baja calidad en los acabados de las piezas", "vibraciones durante el corte", "dificultad para cortar materiales"],
        "falla en sensores de límite": ["lecturas erráticas de posición", "paradas inesperadas de la máquina", "alarmas de límites superados"],
        "falla en el husillo": ["ruido metálico durante la operación", "variaciones en la velocidad del husillo", "sobrecalentamiento en la zona del husillo"],
    }

    print("\nPor favor, responda con 'si', 'no' o 'no sé' a las siguientes preguntas:")
    for diagnostico, sintomas in posibles_sintomas.items():
        for sintoma in sintomas:
            if sintoma not in respuestas:  # Asegurarse de no repetir preguntas ya respondidas.
                respuesta = input(f"¿Presenta el síntoma: {sintoma}? ").strip().lower()
                respuestas[sintoma] = respuesta  # Guardar la respuesta en el diccionario.

    # Calcular porcentajes finales
    resultados = []  # Lista para almacenar los diagnósticos y sus porcentajes calculados.
    for diagnostico, sintomas in posibles_sintomas.items():
        sintomas_confirmados = [sintoma for sintoma in sintomas if respuestas.get(sintoma) == 'si']  # Síntomas confirmados.
        sintomas_no_se = [sintoma for sintoma in sintomas if respuestas.get(sintoma) == 'no sé']  # Síntomas con respuesta 'no sé'.
        sintomas_totales = len(sintomas)  # Total de síntomas asociados al diagnóstico.
        otros_sintomas = [sintoma for sintoma, respuesta in respuestas.items() if respuesta == 'si' and sintoma not in sintomas]  # Síntomas ajenos.

        if sintomas_totales > 0:  # Validar que haya síntomas para calcular porcentaje.
            # Proporción de síntomas confirmados
            porcentaje = (len(sintomas_confirmados) / sintomas_totales) * 100

            # Penalización por síntomas ajenos
            if otros_sintomas:
                penalizacion_ajenos = len(otros_sintomas) * 5  # Penalización fija menor.
                porcentaje -= penalizacion_ajenos

            # Penalización por 'no sé'
            if sintomas_no_se:
                penalizacion_no_se = (len(sintomas_no_se) / sintomas_totales) * 5  # Penalización ajustada.
                porcentaje -= penalizacion_no_se

            # Ajustar porcentaje para evitar valores negativos
            porcentaje = max(0, porcentaje)

            # Agregar el diagnóstico y porcentaje calculado
            resultados.append((diagnostico, porcentaje))

    # Mostrar resultados
    print("\nDiagnósticos finales con porcentaje de probabilidad:")
    if resultados:
        for diagnostico, porcentaje in sorted(resultados, key=lambda x: x[1], reverse=True):
            print(f"- {diagnostico}: {porcentaje:.2f}%")  # Imprimir cada diagnóstico con su porcentaje ordenado de mayor a menor.
    else:
        print("No se encontraron fallas con suficiente probabilidad.")  # Mensaje en caso de no tener resultados.

if __name__ == "__main__":
    main()
