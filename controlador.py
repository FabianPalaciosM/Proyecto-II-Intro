import time
import config
from mapa import generar_mapa_completo
from entidad import Jugador, Enemigo


class ControladorDeJuego:
    def __init__(self, modo_juego):
        self.modo_juego = modo_juego
        self.estado = "jugando"

        self.matriz_numerica, self.matriz_clases = generar_mapa_completo()

        self.jugador = Jugador(0, 0, self.matriz_clases)

        self.enemigos = []
        self.crear_enemigos()

        self.trampas = set()
        self.tiempo_inicio = time.time()

    def crear_enemigos(self):
        cantidad = config.DIFICULTADES[self.modo_juego]["cantidad_de_enemigos"]
        velocidad = config.DIFICULTADES[self.modo_juego]["velocidad_enemigo"]

        for _ in range(cantidad):
            fila, columna = self.buscar_posicion_spawn_enemigo()
            enemigo = Enemigo(fila, columna, self.matriz_clases, self.modo_juego)
            enemigo.velocidad = velocidad
            self.enemigos.append(enemigo)

    def buscar_posicion_spawn_enemigo(self):
        filas = len(self.matriz_clases)
        columnas = len(self.matriz_clases[0])

        for i in range(filas - 1, -1, -1):
            for j in range(columnas - 1, -1, -1):
                if self.matriz_clases[i][j].caminable_por_enemigo():
                    return (i, j)
        return (filas - 1, columnas - 1)

    def mover_jugador(self, dx, dy, correr=False):
        if not self.jugador.vivo or self.estado != "jugando":
            return

        if correr:
            self.jugador.correr(dx, dy)
        else:
            self.jugador.mover(dx, dy)

        if self.jugador.posicion() == (len(self.matriz_clases)-1, len(self.matriz_clases[0])-1):
            self.estado = "victoria"

    def actualizar_enemigos(self):
        if self.estado != "jugando":
            return

        for enemigo in self.enemigos:
            if not enemigo.vivo:
                if enemigo.puede_respawnear():
                    fila, columna = self.buscar_posicion_spawn_enemigo()
                    enemigo.respawnear(fila, columna)
                continue

            fila_enemigo, columna_enemigo = enemigo.posicion()

            if (fila_enemigo, columna_enemigo) in self.trampas:
                enemigo.morir()
                continue

            dx, dy = enemigo.decidir_movimiento(self.jugador)
            enemigo.mover(dx, dy, self.jugador)

            if not self.jugador.vivo:
                self.estado = "derrota"

    def colocar_trampa(self):
        if self.estado != "jugando":
            return False
        
        trampas_actuales = len(self.trampas)

        if self.jugador.colocar_trampa(trampas_actuales):
            fila, columna = self.jugador.posicion()
            self.trampas.add((fila, columna))
            return True
        return False

    def obtener_posicion_jugador(self):
        return self.jugador.posicion()

    def obtener_posiciones_enemigos(self):
        return [enemigo.posicion() for enemigo in self.enemigos if enemigo.vivo]

    def obtener_trampas(self):
        return list(self.trampas)

    def obtener_mapa_render(self):
        return self.matriz_clases

    def estado_juego(self):
        return self.estado
