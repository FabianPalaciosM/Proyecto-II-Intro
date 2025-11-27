import random
import config

def camino_aleatorio(filas, columnas, inicio, final):
    #E: Cantidad de filas y columnas. El inicio y final son tuplas (fila, columna)
    #S: Lista con las coordenadas para llegar al final
    #R:
    #Crea un camino entre el inicio y el final

    ruta = [inicio]
    visitados = {inicio}

    movimientos = [(-1,0), (1,0), (0,-1), (0,1)]

    while ruta[-1] != final:
        fila_actual, columna_actual = ruta[-1]

        opciones = []
        for mov_fila, mov_columna in movimientos:
            nueva_fila = fila_actual + mov_fila
            nueva_columna = columna_actual + mov_columna

            if 0 <= nueva_fila < filas and 0 <= nueva_columna < columnas:
                if (nueva_fila, nueva_columna) not in visitados:
                    opciones.append((nueva_fila, nueva_columna))

        if opciones:
            siguiente = random.choice(opciones)
            ruta.append(siguiente)
            visitados.add(siguiente)
        else:
            ruta.pop()
            if not ruta:
                return camino_aleatorio(filas, columnas, inicio, final)

    return ruta


def matriz_vacia(filas, columnas):
    #E: Cantidad de filas y columnas
    #S: Matriz con None en todas sus casillas
    #R:
    # Crea una matriz con None para ser rellenada después
    return [[None for i in range(columnas)] for j in range(filas)]


def insertar_camino_en_matriz(matriz, ruta):
    #E: La matriz del mapa, la ruta para llegar al final(lista de tuplas)
    #S:
    #R:
    # Mete 0 en las casillas del camino
    for fila, columna in ruta:
        matriz[fila][columna] = 0


def llenar_mapa(matriz):
    #E: La matriz del mapa
    #S:
    #R:
    # Rellena las casillas vacías con valores aleatorios 0–3
    filas = len(matriz)
    columnas = len(matriz[0])

    for fila in range(filas):
        for columna in range(columnas):
            if matriz[fila][columna] is None:
                matriz[fila][columna] = random.randint(0, 3)


def colocar_salida(matriz, final):
    #E: La matriz del mapa. La tupla que representa la salida
    #S:
    #R:
    # Pone 4 en el espacio de la salida para más tarde asignarle una clase especial
    fila, columna = final
    matriz[fila][columna] = 4



def generar_mapa(filas, columnas):
    #E: Cantidad de filas y columnas 
    #S: Matriz final lista con camino, terrenos y salida 
    #R: 
    # # Genera un mapa completo válido con un camino asegurado y una salida
    inicio = (0, 0)
    final = (filas-1, columnas-1)

    matriz = matriz_vacia(filas, columnas)

    ruta = camino_aleatorio(filas, columnas, inicio, final)
    insertar_camino_en_matriz(matriz, ruta)

    llenar_mapa(matriz)

    colocar_salida(matriz, final)

    return matriz
