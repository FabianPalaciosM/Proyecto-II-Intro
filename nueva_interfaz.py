import pygame
from sys import exit
import os
import time
from controlador import ControladorDeJuego
import config
from personajes import personaje_normal, cazador
pygame.init()
pygame.font.init()

ANCHO = 900
ALTO = 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Proyecto Laberinto")

estado_inicio = "inicio"
estado_modo = "modo"
estado_juego = "juego"
estado_pausa = "pausa"
estado_resultado = "resultado"

fuente = pygame.font.SysFont("consolas", 22)
fuente_titulo = pygame.font.SysFont("consolas", 40)

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 200, 0)
ROJO = (200, 0, 0)
AZUL = (0, 150, 255)
GRIS = (60, 60, 60)
GRIS_OSCURO = (40, 40, 40)

controlador = None
jugador = None
enemigos = None
clock = pygame.time.Clock()
tiempo_inicio = 0
TAM_CASILLA = 18


def estilo_casilla(tipo):
    if tipo == 1:
        return (110, 80, 50), (60, 40, 25), (150, 115, 75)
    elif tipo == 2:
        return (20, 90, 60), (10, 50, 30), (40, 130, 80)
    elif tipo == 3:
        return (25, 30, 35), (10, 15, 18), (60, 70, 80)
    elif tipo == 4:
        return (90, 90, 100), (40, 40, 45), (160, 160, 180)
    else:
        return (30, 70, 40), (20, 40, 25), (45, 95, 55)

def dibujar_casilla(surface, x, y, tipo, tam):
    r = pygame.Rect(x, y, tam, tam)

    if tipo == 5:
        pygame.draw.rect(surface, (120, 220, 255), r)
        pygame.draw.rect(surface, (60, 150, 200), r, 2)
        return

    fondo, borde, detalle = estilo_casilla(tipo)
    pygame.draw.rect(surface, fondo, r)
    pygame.draw.rect(surface, borde, r, 1)

    if tipo == 2:
        pygame.draw.rect(surface, detalle, (r.centerx - 2, r.top + 2, 4, r.height - 4))
    elif tipo == 3:
        inner = r.inflate(-6, -6)
        pygame.draw.rect(surface, detalle, inner, 1)
    elif tipo == 4:
        cx, cy = r.centerx, r.centery
        yb = r.bottom - 3
        pygame.draw.line(surface, borde, (r.left + 2, yb), (r.right - 2, yb), 1)
        n = 5
        ap = (r.width - 8) // n
        for i in range(n):
            x1 = r.left + 4 + i * ap
            x3 = x1 + ap - 2
            x2 = (x1 + x3) // 2
            yp = yb - (r.height // 2)
            pygame.draw.polygon(surface, detalle, [(x1, yb), (x3, yb), (x2, yp)])
    else:
        p1 = (r.left + 4, r.centery)
        p2 = (r.centerx, r.top + 4)
        p3 = (r.right - 4, r.centery)
        p4 = (r.centerx, r.bottom - 4)
        pygame.draw.polygon(surface, detalle, [p1, p2, p3, p4], 1)

def dibujar_mapa_backend(surface, controlador, x0, y0, tam):
    mapa = controlador.obtener_mapa()
    filas = len(mapa)
    columnas = len(mapa[0])

    for f in range(filas):
        for c in range(columnas):
            cas = mapa[f][c]
            if cas.tipo == "camino":
                tipo = 0
            elif cas.tipo == "muro":
                tipo = 1
            elif cas.tipo == "liana":
                tipo = 2
            elif cas.tipo == "tunel":
                tipo = 3
            elif cas.tipo == "salida":
                tipo = 5
            else:
                tipo = 0
            dibujar_casilla(surface, x0 + c * tam, y0 + f * tam, tipo, tam)

def dibujar_entidades(surface, controlador, x0, y0, tam):
    j = controlador.jugador
    px = x0 + j.columna * tam
    py = y0 + j.fila * tam
    personaje_normal(surface, px, py)

    for e in controlador.enemigos:
        ex = x0 + e.columna * tam
        ey = y0 + e.fila * tam
        cazador(surface, ex, ey)

def menu_inicio():
    pantalla.fill(NEGRO)
    titulo = fuente_titulo.render("LABERINTO", True, BLANCO)
    sub = fuente.render("Presiona ENTER para continuar", True, BLANCO)
    pantalla.blit(titulo, (ANCHO//2 - titulo.get_width()//2, 200))
    pantalla.blit(sub, (ANCHO//2 - sub.get_width()//2, 320))
    pygame.display.flip()

def menu_modo():
    pantalla.fill(NEGRO)
    t1 = fuente_titulo.render("Selecciona Modo", True, BLANCO)
    o1 = fuente.render("1 - Escapa", True, BLANCO)
    o2 = fuente.render("2 - Cazador", True, BLANCO)
    pantalla.blit(t1, (ANCHO//2 - t1.get_width()//2, 180))
    pantalla.blit(o1, (ANCHO//2 - o1.get_width()//2, 300))
    pantalla.blit(o2, (ANCHO//2 - o2.get_width()//2, 340))
    pygame.display.flip()

def iniciar_partida(modo):
    global controlador, jugador, enemigos, tiempo_inicio
    controlador = ControladorDeJuego(modo)
    jugador = controlador.jugador
    enemigos = controlador.enemigos
    tiempo_inicio = time.time()

def estado_juego_loop():
    global estado_actual

    dt = clock.tick(60) / 1000

    keys = pygame.key.get_pressed()
    dx = dy = 0

    if keys[pygame.K_w]: dx, dy = -1, 0
    elif keys[pygame.K_s]: dx, dy = 1, 0
    elif keys[pygame.K_a]: dx, dy = 0, -1
    elif keys[pygame.K_d]: dx, dy = 0, 1

    if dx != 0 or dy != 0:
        controlador.mover_jugador(dx, dy)

    controlador.actualizar_enemigos(dt)

    resultado = controlador.estado_partida()
    if resultado == "victoria":
        estado_actual = estado_resultado
        return
    elif resultado == "derrota":
        estado_actual = estado_resultado
        return

    pantalla.fill((20, 20, 20))

    ancho_mapa = config.CANTIDAD_DE_COLUMNAS * TAM_CASILLA
    alto_mapa = config.CANTIDAD_DE_FILAS * TAM_CASILLA

    x0 = ANCHO // 2 - ancho_mapa // 2
    y0 = ALTO // 2 - alto_mapa // 2 + 20

    dibujar_mapa_backend(pantalla, controlador, x0, y0, TAM_CASILLA)
    dibujar_entidades(pantalla, controlador, x0, y0, TAM_CASILLA)

    energia_txt = fuente.render(f"Energia: {controlador.jugador.energia}", True, BLANCO)
    pantalla.blit(energia_txt, (20, 20))

    tiempo_actual = int(time.time() - tiempo_inicio)
    tiempo_txt = fuente.render(f"Tiempo: {tiempo_actual}s", True, BLANCO)
    pantalla.blit(tiempo_txt, (20, 50))

    pausa_txt = fuente.render("P - Pausa", True, BLANCO)
    pantalla.blit(pausa_txt, (20, 80))

    pygame.display.flip()


def estado_pausa_loop():
    global estado_actual

    pantalla.fill((10, 10, 10))

    t1 = fuente_titulo.render("PAUSA", True, BLANCO)
    t2 = fuente.render("ENTER - Continuar", True, BLANCO)
    t3 = fuente.render("ESC - Menu principal", True, BLANCO)

    pantalla.blit(t1, (ANCHO//2 - t1.get_width()//2, 220))
    pantalla.blit(t2, (ANCHO//2 - t2.get_width()//2, 320))
    pantalla.blit(t3, (ANCHO//2 - t3.get_width()//2, 360))

    pygame.display.flip()


def estado_resultado_loop():
    global estado_actual

    pantalla.fill((0, 0, 0))

    resultado = controlador.estado_partida()
    tiempo_total = int(time.time() - tiempo_inicio)

    if resultado == "victoria":
        msg = "VICTORIA"
        color = AZUL
    else:
        msg = "DERROTA"
        color = ROJO

    t1 = fuente_titulo.render(msg, True, color)
    pantalla.blit(t1, (ANCHO//2 - t1.get_width()//2, 200))

    t2 = fuente.render(f"Tiempo total: {tiempo_total} s", True, BLANCO)
    pantalla.blit(t2, (ANCHO//2 - t2.get_width()//2, 290))

    t3 = fuente.render("ENTER - Volver al menu", True, BLANCO)
    pantalla.blit(t3, (ANCHO//2 - t3.get_width()//2, 350))

    pygame.display.flip()


def main():
    global estado_actual
    estado_actual = estado_inicio

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:

                if estado_actual == estado_inicio:
                    if event.key == pygame.K_RETURN:
                        estado_actual = estado_modo

                elif estado_actual == estado_modo:
                    if event.key == pygame.K_1:
                        iniciar_partida("escapa")
                        estado_actual = estado_juego
                    elif event.key == pygame.K_2:
                        iniciar_partida("cazador")
                        estado_actual = estado_juego

                elif estado_actual == estado_juego:
                    if event.key == pygame.K_p:
                        estado_actual = estado_pausa

                elif estado_actual == estado_pausa:
                    if event.key == pygame.K_RETURN:
                        estado_actual = estado_juego
                    elif event.key == pygame.K_ESCAPE:
                        estado_actual = estado_inicio

                elif estado_actual == estado_resultado:
                    if event.key == pygame.K_RETURN:
                        estado_actual = estado_inicio

        if estado_actual == estado_inicio:
            menu_inicio()

        elif estado_actual == estado_modo:
            menu_modo()

        elif estado_actual == estado_juego:
            estado_juego_loop()

        elif estado_actual == estado_pausa:
            estado_pausa_loop()

        elif estado_actual == estado_resultado:
            estado_resultado_loop()


if __name__ == "__main__":
    main()
