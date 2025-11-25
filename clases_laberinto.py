class Casilla:
    def __init__(self, fila, columna, tipo):
        #La fila y columna de la casilla, el tipo que es (camino, liana, etc. )
        self.fila = fila
        self.columna = columna
        self.tipo = tipo

    def caminable_por_jugador(self):
        #True o False si el jugador puede pasar por ella
        raise NotImplementedError("No esta hecho")

    def caminable_por_enemigo(self):
        #True o False si el enemigo puede pasar por ella
        raise NotImplementedError("No esta hecho")

    def __str__(self):
        return f"{self.tipo} en la casilla[{self.fila}][{self.columna}]"
    
casi = Casilla(1,1,"liana")
casi.caminable_por_enemigo()

class Camino(Casilla):
    def __init__(self, fila, columna):
        super().__init__(fila, columna, "camino")

    def caminable_por_jugador(self):
        return True

    def caminable_por_enemigo(self):
        return True
    
    
class Muro(Casilla):
    def __init__(self, fila, columna):
        super().__init__(fila, columna, "muro")

    def caminable_por_jugador(self):
        return False

    def caminable_por_enemigo(self):
        return False
    
class Liana(Casilla):
    def __init__(self, fila, columna):
        super().__init__(fila, columna, "liana")

    def caminable_por_jugador(self):
        return False

    def caminable_por_enemigo(self):
        return True
    
class Tunel(Casilla):
    def __init__(self, fila, columna):
        super().__init__(fila, columna, "tunel")

    def caminable_por_jugador(self):
        return True

    def caminable_por_enemigo(self):
        return False
    