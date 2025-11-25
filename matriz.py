import random

def generar_matriz_nula(filas, columnas):
    #E: Cantidad (int) de filas y columnas de la matriz
    #S: Una matriz
    #Crea una matriz nula, con 0 en todos sus espacios
    matriz=[]
    for i in range(filas):
        fila=[]
        for j in range(columnas):
            fila.append(0)
        matriz.append(fila)
    print(matriz)  
    print() 
    return matriz
mmmatriz = generar_matriz_nula(10,10)

def camino_aleatorio(matriz, punto_inicio, punto_final):
    n = len(matriz)
    ruta = [punto_inicio]
    posicion_actual = punto_inicio
    visitados = {punto_inicio}

    while posicion_actual != punto_final:
        fila, columna = posicion_actual

        opciones = []
        if fila > 0:
            opciones.append((fila - 1, columna))
        if fila < n - 1:
            opciones.append((fila + 1, columna))
        if columna > 0:
            opciones.append((fila, columna - 1))
        if columna < len(matriz[0]) - 1:
            opciones.append((fila, columna + 1))

        opciones_validas = [p for p in opciones if p not in visitados]

        if opciones_validas:
            random.shuffle(opciones_validas)
            siguiente = opciones_validas[0]
            ruta.append(siguiente)
            visitados.add(siguiente)
            posicion_actual = siguiente
        else:
            ruta.pop()
            posicion_actual = ruta[-1]

    return ruta

def reemplazar_espacios(matriz, lista_no_reemplazables):
    filas = len(matriz)
    columnas = len(matriz[0])
    nueva_matriz = []
    posiciones_no_reemplazables = set(lista_no_reemplazables)

    for i in range(filas):
        fila = []
        for j in range(columnas):
            if (i, j) in posiciones_no_reemplazables:
                fila.append(matriz[i][j])  # mantiene el 0 
            else:
                fila.append(random.randint(0, 3))
        nueva_matriz.append(fila)

    return nueva_matriz


print(reemplazar_espacios(mmmatriz, camino_aleatorio(mmmatriz,(0,0), (9,9))))