import time
import config
import random
from mapa import generar_mapa_completo
from entidad import Jugador, Enemigo


class ControladorDeJuego:
    def __init__(self, dificultad, modo_juego):
        self.dificultad = dificultad
        self.modo_juego = modo_juego
        self.estado = "jugando"

        self.matriz_numerica, self.matriz_clases = generar_mapa_completo()

        if modo_juego == "cazador":
            posicion_salida = self.buscar_salida()
            self.jugador = Jugador(posicion_salida[0], posicion_salida[1], self.matriz_clases)
        else:
            self.jugador = Jugador(0, 0, self.matriz_clases)

        self.enemigos = []
        self.crear_enemigos()

        self.trampas = set()
        self.tiempo_inicio = time.time()
        self.ultimo_movimiento_enemigos = time.time()
        self.ultimo_movimiento_jugador = time.time()
        self.enemigos_eliminados = 0
        self.enemigos_capturados = 0
        self.enemigos_escapados = 0

    def crear_enemigos(self):
        #Crea los enemigos en el mapa
        cantidad = config.DIFICULTADES[self.dificultad]["cantidad_de_enemigos"]
        velocidad = config.DIFICULTADES[self.dificultad]["velocidad_enemigo"]

        for _ in range(cantidad):
            fila, columna = self.buscar_posicion_spawn_enemigo()
            enemigo = Enemigo(fila, columna, self.matriz_clases, self.modo_juego)
            enemigo.velocidad = velocidad
            self.enemigos.append(enemigo)

    def buscar_salida(self):
        #Busca la salida
        filas = len(self.matriz_clases)
        columnas = len(self.matriz_clases[0])

        for i in range(filas):
            for j in range(columnas):
                if self.matriz_clases[i][j].es_salida():
                    return (i, j)
        return (filas - 1, columnas - 1)

    def buscar_posicion_spawn_enemigo(self):
        #Busca una casilla donde pueda estar el enemigo
        filas = len(self.matriz_clases)
        columnas = len(self.matriz_clases[0])

        posiciones_validas = []
        for i in range(filas):
            for j in range(columnas):
                if self.matriz_clases[i][j].caminable_por_enemigo():
                    posiciones_validas.append((i, j))

        if posiciones_validas:
            return random.choice(posiciones_validas)
        return (filas - 1, columnas - 1)

    def mover_jugador(self, dx, dy, correr=False):
        #Mueve el jugador
        if not self.jugador.vivo or self.estado != "jugando":
            return False

        tiempo_actual = time.time()
        velocidad_requerida = self.jugador.velocidad_correr if correr else self.jugador.velocidad_caminar

        if tiempo_actual - self.ultimo_movimiento_jugador < velocidad_requerida:
            return False

        movido = False
        if correr:
            movido = self.jugador.correr(dx, dy)
        else:
            movido = self.jugador.mover(dx, dy)

        if movido:
            self.ultimo_movimiento_jugador = tiempo_actual

            fila, columna = self.jugador.posicion()
            casilla_actual = self.matriz_clases[fila][columna]
            if casilla_actual.es_salida():
                self.estado = "victoria"

        return movido

    def verificar_colision_adyacente(self, pos_jugador, pos_enemigo):
        #Verifica que el jugador y el enemigo no estén a la par
        fila_j, col_j = pos_jugador
        fila_e, col_e = pos_enemigo

        diferencia_fila = abs(fila_j - fila_e)
        diferencia_col = abs(col_j - col_e)

        return (diferencia_fila <= 1 and diferencia_col <= 1 and not (diferencia_fila == 0 and diferencia_col == 0))

    def actualizar_enemigos(self):
        #Actualiza la posición de los enemigos
        if self.estado != "jugando":
            return

        tiempo_actual = time.time()

        for enemigo in self.enemigos:
            if not enemigo.vivo:
                if enemigo.puede_respawnear():
                    fila, columna = self.buscar_posicion_spawn_enemigo()
                    enemigo.respawnear(fila, columna)
                continue

            fila_enemigo, columna_enemigo = enemigo.posicion()

            if (fila_enemigo, columna_enemigo) in self.trampas:
                enemigo.morir()
                self.trampas.discard((fila_enemigo, columna_enemigo))
                self.enemigos_eliminados += 1
                continue

            if tiempo_actual - self.ultimo_movimiento_enemigos >= enemigo.velocidad:
                dx, dy = enemigo.decidir_movimiento(self.jugador)
                enemigo.mover(dx, dy, self.jugador)

            pos_jugador = self.jugador.posicion()
            pos_enemigo = enemigo.posicion()

            if self.modo_juego == "escapa":
                if (pos_jugador == pos_enemigo or
                    self.verificar_colision_adyacente(pos_jugador, pos_enemigo)):
                    self.jugador.morir()
                    self.estado = "derrota"
                    break
            else:
                casilla_enemigo = self.matriz_clases[fila_enemigo][columna_enemigo]
                if casilla_enemigo.es_salida():
                    enemigo.morir()
                    self.enemigos_escapados += 1
                    continue

                if (pos_jugador == pos_enemigo or
                    self.verificar_colision_adyacente(pos_jugador, pos_enemigo)):
                    enemigo.morir()
                    self.enemigos_capturados += 1

        if self.modo_juego == "cazador":
            enemigos_vivos = sum(1 for e in self.enemigos if e.vivo)
            if enemigos_vivos == 0:
                self.estado = "victoria"

        if tiempo_actual - self.ultimo_movimiento_enemigos >= min([e.velocidad for e in self.enemigos if e.vivo], default=0.4):
            self.ultimo_movimiento_enemigos = tiempo_actual

    def colocar_trampa(self):
        #Coloca una trampa en el mapa en tiempo de ejecución
        if self.estado != "jugando":
            return False
        
        trampas_actuales = len(self.trampas)

        if self.jugador.colocar_trampa(trampas_actuales):
            fila, columna = self.jugador.posicion()
            self.trampas.add((fila, columna))
            return True
        return False

    def obtener_posicion_jugador(self):
        #Retorna la posicion del jugador
        return self.jugador.posicion()

    def obtener_posiciones_enemigos(self):
        #Retorna la posicion de los enemigos
        return [enemigo.posicion() for enemigo in self.enemigos if enemigo.vivo]

    def obtener_trampas(self):
        #Retorna una lista de tramoas
        return list(self.trampas)

    def obtener_mapa_render(self):
        #Retorna el mapa
        return self.matriz_clases

    def obtener_enemigos_eliminados(self):
        #Retorna la cantidad de enemigos eliminados
        return self.enemigos_eliminados

    def obtener_enemigos_capturados(self):
        #Retorna la cantidad de enemigos capturados
        return self.enemigos_capturados

    def obtener_enemigos_escapados(self):
        #Retorna la cantidad de enemigos escapados
        return self.enemigos_escapados

    def estado_juego(self):
        #Retorna el estado del juego 
        return self.estado
