import json

with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)


CANTIDAD_DE_FILAS = data.get("cantidad_de_filas")
CANTIDAD_DE_COLUMNAS = data.get("cantidad_de_columnas")
ENERGIA_INICIAL = data.get("energia_inicial")
ENERGIA_GASTADA_CORRIENDO = data.get("energia_gastada_corriendo")
ENERGIA_RECUPERADA = data.get("energia_recuperada")
CANTIDAD_TRAMPAS = data.get("cantidad_trampas")
COOLDOWN_TRAMPAS = data.get("cooldown_trampas")
TIEMPO_RESPAWNEO_ENEMIGOS = data.get("tiempo_respawneo_enemigos")
VELOCIDAD_JUGADOR = data.get("velocidad_jugador")
VELOCIDAD_JUGADOR_CORRIENDO = data.get("velocidad_jugador_corriendo")
DIFICULTADES = data.get("dificultad")   
PUNTAJE = data.get("puntaje")

def obtener_dificultad(nivel):
    #Retorna los parametros especificos de la dificultad seleccionada
    return DIFICULTADES.get(nivel, None)