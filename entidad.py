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
        #Cambia el estado a muerto 
        self.vivo = False

    def puede_entrar(self, casilla):
        #Revisa si puede entrar a una casilla
        return casilla.caminable_por_jugador()

    def mover(self, dx, dy):
        #Mueve el personaje a la casilla destino
        casilla_destino = self.intentar_mover(dx, dy)
        if casilla_destino is False:
            return False
        self.fila += dx
        self.columna += dy
        return True

    def activar_correr(self):
        #Cambia la velocidad actual por la de correr y viceversa para moverse más rápido
        if self.energia > 0:
            self.velocidad_actual = self.velocidad_correr
        else:
            self.velocidad_actual = self.velocidad_caminar

    def desactivar_correr(self):
        #Cambia la velocidad actual a la velocidad caminando
        self.velocidad_actual = self.velocidad_caminar

    def correr(self, dx, dy):
        #Valida la energía del jugador, corre y drena la energía
        if self.energia <= 0:
            self.desactivar_correr()
            return self.mover(dx, dy)
        self.activar_correr()
        self.energia -= config.ENERGIA_GASTADA_CORRIENDO
        if self.energia < 0:
            self.energia = 0
        return self.mover(dx, dy)

    def recuperar_energia(self):
        #Recupera la energía después de usarla
        self.energia += config.ENERGIA_RECUPERADA
        if self.energia > config.ENERGIA_INICIAL:
            self.energia = config.ENERGIA_INICIAL

    def puede_colocar_trampa(self, trampas_en_mapa):
        #Revisa si se puede colocar una trampa por el cooldown y cantidad de trampas en mapa
        tiempo_actual = time.time()
        if trampas_en_mapa >= config.CANTIDAD_TRAMPAS:
            return False
        if tiempo_actual - self.tiempo_ultima_trampa < config.COOLDOWN_TRAMPAS:
            return False
        return True

    def colocar_trampa(self, trampas_en_mapa):
        #Coloca la trampa en el mapa
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
        #Revisa si puede entrar a una casilla
        if casilla.tipo == "muro":
            return False
        if casilla.tipo == "tunel":
            return False
        if casilla.tipo == "salida":
            return False
        return casilla.caminable_por_enemigo()

    def mover(self, dx, dy, jugador):
        #Mueve al enemigo
        if not self.vivo:
            return False

        casilla_destino = self.intentar_mover(dx, dy)
        if casilla_destino is False:
            direcciones_alternativas = []
            if dx == 0:
                direcciones_alternativas = [(1, 0), (-1, 0), (0, -dy)]
            elif dy == 0:
                direcciones_alternativas = [(0, 1), (0, -1), (-dx, 0)]

            for alt_dx, alt_dy in direcciones_alternativas:
                casilla_alt = self.intentar_mover(alt_dx, alt_dy)
                if casilla_alt is not False:
                    dx, dy = alt_dx, alt_dy
                    casilla_destino = casilla_alt
                    break

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
        #Cambia vivo a False
        self.vivo = False
        self.tiempo_muerte = time.time()

    def puede_respawnear(self):
        #Respawnea un enemigo muerto después de x cantidad de segundos
        if not self.vivo:
            tiempo_transcurrido = time.time() - self.tiempo_muerte
            return tiempo_transcurrido >= config.TIEMPO_RESPAWNEO_ENEMIGOS
        return False

    def respawnear(self, fila, columna):
        #Respawnea el enemigo y cambia se estado vivo a True
        self.fila = fila
        self.columna = columna
        self.vivo = True

    def decidir_movimiento(self, jugador):
        #Dependiendo del modo decide a que casilla moverse según su posición
        if not self.vivo:
            return (0, 0)

        dx = 0
        dy = 0

        if self.modo == "escapa":
            fila_jugador, columna_jugador = jugador.posicion()

            if fila_jugador > self.fila:
                dx = 1
            elif fila_jugador < self.fila:
                dx = -1
            elif columna_jugador > self.columna:
                dy = 1
            elif columna_jugador < self.columna:
                dy = -1

        else:
            salida_fila, salida_columna = self.buscar_salida_cercana()

            if salida_fila > self.fila:
                dx = 1
            elif salida_fila < self.fila:
                dx = -1
            elif salida_columna > self.columna:
                dy = 1
            elif salida_columna < self.columna:
                dy = -1

        return (dx, dy)

    def buscar_salida_cercana(self):
        #Busca la salida 
        filas = len(self.mapa)
        columnas = len(self.mapa[0])

        for i in range(filas):
            for j in range(columnas):
                if self.mapa[i][j].es_salida():
                    return (i, j)
        return (filas - 1, columnas - 1)
