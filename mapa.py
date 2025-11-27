from clases_laberinto import Camino, Liana, Tunel, Muro, Salida
import config
from matriz import generar_mapa 


mapa_numerico = generar_mapa(config.CANTIDAD_DE_FILAS, config.CANTIDAD_DE_COLUMNAS)

def generar_matriz_clases():
    global mapa_numerico

    filas = len(mapa_numerico)
    columnas = len(filas)

    matriz = []
    for i in range(filas):
        for j in range(columnas):
            pass