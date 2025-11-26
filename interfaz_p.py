import pygame
from sys import exit
from personajes import personaje_normal, cazador

ancho, alto = 900, 600
fps = 30

color_fondo1 = (12, 20, 14)
color_fondo2 = (20, 28, 22)
color_frame = (70, 80, 22)
color_frame_i = (30, 35, 30)
color_btn = (60, 70, 60)
color_btn_h = (100, 120, 80)
color_btn_b = (200, 190, 140)
color_texto = (235, 230, 210)
color_texto2 = (180, 175, 150)

pygame.init()
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Escapa del laberinto")
clock = pygame.time.Clock()
fuente_titulo = pygame.font.SysFont("consolas", 52, bold=True)
fuente_subt = pygame.font.SysFont("consolas", 22)
fuente_btn = pygame.font.SysFont("consolas", 26)

estado_menu = "menu"
estado_registro = "registro"
estado_puntajes = "puntajes"
estado = estado_menu

pixel_bg = pygame.Surface((ancho, alto))
tam_cuadro = 16

for i in range(0, ancho, tam_cuadro):
    for j in range(0, alto, tam_cuadro):
        if (i // tam_cuadro + j // tam_cuadro) % 2 == 0:
            pixel_bg.fill(color_fondo1, (i, j, tam_cuadro, tam_cuadro))
        else:
            pixel_bg.fill(color_fondo2, (i, j, tam_cuadro, tam_cuadro))


def dibujar_texto(surface, texto, fuente, color, x, y, centro=True):
    render = fuente.render(texto, True, color)
    rect = render.get_rect()
    if centro:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(render, rect)
    return rect


def dibujar_marco(surface):
    margen = 32
    rect_externo = pygame.Rect(margen, margen, ancho - 2 * margen, alto - 2 * margen)
    pygame.draw.rect(surface, color_frame, rect_externo, width=4)

    margen_i = 52
    rect_interno = pygame.Rect(
        margen_i, margen_i,
        ancho - 2 * margen_i,
        alto - 2 * margen_i
    )

    pygame.draw.rect(surface, color_frame_i, rect_interno, width=0)
    pygame.draw.rect(surface, color_frame, rect_interno, width=3)
    return rect_interno


def dibujar_boton(surface, texto, x, y, ancho_btn, alto_btn, mouse_pos):
    rect_btn = pygame.Rect(x, y, ancho_btn, alto_btn)
    if rect_btn.collidepoint(mouse_pos):
        color_actual = color_btn_h
    else:
        color_actual = color_btn

    pygame.draw.rect(surface, color_actual, rect_btn, border_radius=0)
    pygame.draw.rect(surface, color_btn_b, rect_btn, 3)
    inner = rect_btn.inflate(-6, -6)
    pygame.draw.rect(surface, (40, 20, 70), inner, 2)

    dibujar_texto(surface, texto, fuente_btn, color_texto,
                  rect_btn.centerx, rect_btn.centery)
    return rect_btn


corriendo = True
while corriendo:
    dt = clock.tick(fps) / 1000
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False
        elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_click = True

    pantalla.blit(pixel_bg, (0, 0))

    if estado == estado_menu:
        rect_interno = dibujar_marco(pantalla)

        dibujar_texto(
            pantalla, "ESCAPA DEL LABERINTO",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 80
        )

        dibujar_texto(
            pantalla, "¡Sobrevive y escapa!",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.top + 130
        )

        btn_ancho = 260
        btn_alto = 56
        espacio_v = 18

        x_btn = (ancho - btn_ancho) // 2
        y_btn_inicio = rect_interno.top + 162

        btn_jugar = dibujar_boton(
            pantalla, "JUGAR",
            x_btn, y_btn_inicio,
            btn_ancho, btn_alto, mouse_pos
        )

        btn_registro = dibujar_boton(
            pantalla, "REGISTRO",
            x_btn, y_btn_inicio + (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos
        )

        btn_puntajes = dibujar_boton(
            pantalla, "PUNTAJES",
            x_btn, y_btn_inicio + 2 * (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos
        )

        btn_salir = dibujar_boton(
            pantalla, "SALIR",
            x_btn, y_btn_inicio + 3 * (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos
        )

        dibujar_texto(
            pantalla, " Fabi y Nico - 2025",
            fuente_subt, (220, 210, 160),
            ancho // 2,
            rect_interno.bottom - 30
        )

        if mouse_click:
            if btn_jugar.collidepoint(mouse_pos):
                estado = estado_registro
            elif btn_registro.collidepoint(mouse_pos):
                estado = estado_registro
            elif btn_puntajes.collidepoint(mouse_pos):
                estado = estado_puntajes
            elif btn_salir.collidepoint(mouse_pos):
                corriendo = False

    elif estado == estado_registro:
        rect_interno = dibujar_marco(pantalla)
        dibujar_texto(
            pantalla, "Registro de Jugador",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 120
        )
        # Aquí va lógica del registro

        dibujar_texto(
            pantalla, "Cuadro nombre del jugador",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.top + 180
        )
        dibujar_texto(
            pantalla, "Presiona ESC para regresar al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu

    elif estado == estado_puntajes:
        rect_interno = dibujar_marco(pantalla)
        dibujar_texto(
            pantalla, "Tabla de Puntajes",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 90
        )
        # Aquí va lógica de puntajes

        dibujar_texto(
            pantalla, "Cuadro de puntajes",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.top + 170
        )
        dibujar_texto(
            pantalla, "Presiona ESC para regresar al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu

    pygame.display.flip()

pygame.quit()
exit()
