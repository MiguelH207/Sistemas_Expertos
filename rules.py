def evaluate_facts(facts):
    """Evalúa los hechos contra la base de reglas."""
    # Base de reglas
    rules = {
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

    for fallo, sintomas in rules.items():
        if all(sintoma in facts for sintoma in sintomas):
            return fallo

    return None
