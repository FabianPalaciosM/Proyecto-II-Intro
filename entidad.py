from clases_laberinto import Camino, Liana, Tunel, Muro, Salida
import time
import config

    
class Entidad:
    def __init__(self, fila, columna, velocidad, mapa):
        self.fila = fila
        self.columna = columna
        self.velocidad = velocidad
        self.mapa = mapa

    def posicion(self):
        #Retorna la posición actual de la entidad
        return (self.fila, self.columna)
    
    def dentro_de_limites(self, fila, columna):
        #Revisa si la fila y la columna ingresadas están dentro del mapa jugable
        filas_totales = len(self.mapa)
        columnas_totales = len(self.mapa[0])
        return 0 <= fila < filas_totales and 0 <= columna < columnas_totales

    def puede_entrar(self, casilla):
        #Revisa si se puede entrar en la casilla, lo valida cada subclase
        raise NotImplementedError

    def intentar_mover(self, dx, dy):
        #Revisa cual serpia la fila y columna a la que se va a mover la entidad, valida los limites pero no valida si esta puede moverse allí
        nueva_fila = self.fila + dx
        nueva_columna = self.columna + dy

        if not self.dentro_de_limites(nueva_fila, nueva_columna):
            return False

        casilla_destino = self.mapa[nueva_fila][nueva_columna]

        if not self.puede_entrar(casilla_destino): #Si la casilla permite entrar
            return False

        return casilla_destino


class Jugador(Entidad):
    def __init__(self, fila, columna, mapa):
        super().__init__(fila, columna, config.VELOCIDAD_JUGADOR, mapa)
        self.velocidad_caminar = config.VELOCIDAD_JUGADOR
        self.velocidad_correr = config.VELOCIDAD_JUGADOR_CORRIENDO
        self.velocidad_actual = self.velocidad_caminar
        self.energia = config.ENERGIA_INICIAL
        self.tiempo_ultima_trampa = 0
        self.vivo = True


    def morir(self):
        self.vivo = False

    def puede_entrar(self, casilla):
        return casilla.caminable_por_jugador()

    def mover(self, dx, dy):
        casilla_destino = self.intentar_mover(dx, dy)
        if casilla_destino is False:
            return False
        self.fila += dx
        self.columna += dy
        return True

    def activar_correr(self):
        if self.energia > 0:
            self.velocidad_actual = self.velocidad_correr
        else:
            self.velocidad_actual = self.velocidad_caminar

    def desactivar_correr(self):
        self.velocidad_actual = self.velocidad_caminar

    def correr(self, dx, dy):
        if self.energia <= 0:
            self.desactivar_correr()
            return self.mover(dx, dy)
        self.activar_correr()
        self.energia -= config.ENERGIA_GASTADA_CORRIENDO
        if self.energia < 0:
            self.energia = 0
        return self.mover(dx, dy)

    def recuperar_energia(self):
        self.energia += config.ENERGIA_RECUPERADA
        if self.energia > config.ENERGIA_INICIAL:
            self.energia = config.ENERGIA_INICIAL

    def puede_colocar_trampa(self, trampas_en_mapa):
        tiempo_actual = time.time()
        if trampas_en_mapa >= config.CANTIDAD_TRAMPAS:
            return False
        if tiempo_actual - self.tiempo_ultima_trampa < config.COOLDOWN_TRAMPAS:
            return False
        return True

    def colocar_trampa(self, trampas_en_mapa):
        if not self.puede_colocar_trampa(trampas_en_mapa):
            return False
        self.tiempo_ultima_trampa = time.time()
        return True


class Enemigo(Entidad):
    def __init__(self, fila, columna, mapa, modo):
        super().__init__(fila, columna, config.VELOCIDAD_ENEMIGO, mapa)
        self.modo = modo
        self.vivo = True
        self.tiempo_muerte = 0

    def puede_entrar(self, casilla):
        if casilla.tipo == "muro":
            return False
        if casilla.tipo == "tunel":
            return False
        if casilla.tipo == "salida":
            return False
        return casilla.caminable_por_enemigo()

    def mover(self, dx, dy, jugador):
        if not self.vivo:
            return False

        casilla_destino = self.intentar_mover(dx, dy)
        if casilla_destino is False:
            return False

        self.fila += dx
        self.columna += dy

        if (self.fila, self.columna) == jugador.posicion():
            if self.modo == "escapa":
                jugador.morir()
            else:
                self.morir()

        return True

    def morir(self):
        self.vivo = False
        self.tiempo_muerte = time.time()

    def puede_respawnear(self):
        if not self.vivo:
            tiempo_transcurrido = time.time() - self.tiempo_muerte
            return tiempo_transcurrido >= config.TIEMPO_RESPAWNEO_ENEMIGOS
        return False

    def respawnear(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.vivo = True

    def decidir_movimiento(self, jugador):
        if not self.vivo:
            return (0, 0)

        fila_jugador, columna_jugador = jugador.posicion()

        dx = 0
        dy = 0

        if self.modo == "escapa":
            if fila_jugador > self.fila:
                dx = 1
            elif fila_jugador < self.fila:
                dx = -1
            elif columna_jugador > self.columna:
                dy = 1
            elif columna_jugador < self.columna:
                dy = -1

        else:
            if fila_jugador > self.fila:
                dx = -1
            elif fila_jugador < self.fila:
                dx = 1
            elif columna_jugador > self.columna:
                dy = -1
            elif columna_jugador < self.columna:
                dy = 1

        return (dx, dy)
