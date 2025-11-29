from clases_laberinto import Camino, Liana, Tunel, Muro, Salida
import config
from matriz import generar_mapa 


def convertir_matriz_a_clases(matriz_numerica):
    #E: La matriz numerica 
    #S: La matriz con la clase respectiva en cada espacio
    filas = len(matriz_numerica)
    columnas = len(matriz_numerica[0])

    matriz_clases = [[None for j in range(columnas)] for i in range(filas)]


    for i in range(filas):
        for j in range(columnas):
            if matriz_numerica[i][j] == 0:
                matriz_clases[i][j] = Camino(i, j)
            elif matriz_numerica[i][j] == 1:
                matriz_clases[i][j] = Liana(i, j)
            elif matriz_numerica[i][j] == 2:
                matriz_clases[i][j] = Tunel(i, j)
            elif matriz_numerica[i][j] == 3:
                matriz_clases[i][j] = Muro(i, j)
            elif matriz_numerica[i][j] == 4:
                matriz_clases[i][j] = Salida(i, j)

    return matriz_clases



def generar_mapa_completo():
    matriz_numerica = generar_mapa(config.CANTIDAD_DE_FILAS, config.CANTIDAD_DE_COLUMNAS)

    matriz_de_clases = convertir_matriz_a_clases(matriz_numerica)

    return matriz_numerica, matriz_de_clases