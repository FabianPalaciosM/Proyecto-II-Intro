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

estado_menu  = "menu"
estado_nombre = "nombre"
estado_modo  = "modo"
estado_dificultad  = "dificultad"
estado_puntajes = "puntajes"
estado_juego = "juego"

estado = estado_menu

nombre_jugador = ""
input_activo = False
rol_elegido = ""     
dificultad = ""     

pixel_bg = pygame.Surface((ancho, alto))
tam_cuadro = 16

for i in range(0, ancho, tam_cuadro):
    for j in range(0, alto, tam_cuadro):
        if (i // tam_cuadro + j // tam_cuadro) % 2 == 0:
            pixel_bg.fill(color_fondo1, (i, j, tam_cuadro, tam_cuadro))
        else:
            pixel_bg.fill(color_fondo2, (i, j, tam_cuadro, tam_cuadro))

INPUT_ANCHO = 320
INPUT_ALTO = 40
ALTURA_TEXTO = fuente_subt.get_height()
ESPACIO_TEXTO_INPUT = 15
ALTURA_BLOQUE = ALTURA_TEXTO + ESPACIO_TEXTO_INPUT + INPUT_ALTO
Y_BLOQUE_TOP = alto // 2 - ALTURA_BLOQUE // 2 - 60
Y_SUBTITULO_NOMBRE = Y_BLOQUE_TOP + ALTURA_TEXTO // 2
Y_INPUT_NOMBRE = Y_BLOQUE_TOP + ALTURA_TEXTO + ESPACIO_TEXTO_INPUT
X_INPUT_NOMBRE = ancho // 2 - INPUT_ANCHO // 2
input_rect_nombre = pygame.Rect(X_INPUT_NOMBRE, Y_INPUT_NOMBRE, INPUT_ANCHO, INPUT_ALTO)


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


def dibujar_boton(
    surface, texto, x, y, ancho_btn, alto_btn, mouse_pos,
    color_base=None, color_hover=None, color_borde=None, color_inner=None
):
    if color_base is None:
        color_base = color_btn
    if color_hover is None:
        color_hover = color_btn_h
    if color_borde is None:
        color_borde = color_btn_b
    if color_inner is None:
        color_inner = (40, 20, 70)

    rect_btn = pygame.Rect(x, y, ancho_btn, alto_btn)
    if rect_btn.collidepoint(mouse_pos):
        color_actual = color_hover
    else:
        color_actual = color_base

    pygame.draw.rect(surface, color_actual, rect_btn, border_radius=0)
    pygame.draw.rect(surface, color_borde, rect_btn, 3)
    inner = rect_btn.inflate(-6, -6)
    pygame.draw.rect(surface, color_inner, inner, 2)

    dibujar_texto(surface, texto, fuente_btn, color_texto,
                  rect_btn.centerx, rect_btn.centery)
    return rect_btn


def dibujar_personaje_escalado(func_personaje, surface, center_x, y_top, escala=2.5):
            base_ancho, base_alto = 40, 60 
            temp = pygame.Surface((base_ancho, base_alto), pygame.SRCALPHA)

            func_personaje(temp, 0, 0)

            nuevo_tam = (int(base_ancho * escala), int(base_alto * escala))
            sprite = pygame.transform.scale(temp, nuevo_tam)

            rect = sprite.get_rect(midtop=(center_x, y_top))
            surface.blit(sprite, rect)
            return rect


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
            if estado == estado_nombre:
                if input_rect_nombre.collidepoint(mouse_pos):
                    input_activo = True
                else:
                    input_activo = False

        if estado == estado_nombre and evento.type == pygame.KEYDOWN and input_activo:
            if evento.key == pygame.K_BACKSPACE:
                nombre_jugador = nombre_jugador[:-1]
            else:
                if len(nombre_jugador) < 12 and evento.unicode.isprintable():
                    nombre_jugador += evento.unicode

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

        num_btn = 3
        altura_total = num_btn * btn_alto + (num_btn - 1) * espacio_v
        y_btn_inicio = rect_interno.centery - altura_total // 2

        btn_jugar = dibujar_boton(
            pantalla, "JUGAR",
            x_btn, y_btn_inicio,
            btn_ancho, btn_alto, mouse_pos
        )

        btn_puntajes = dibujar_boton(
            pantalla, "PUNTAJES",
            x_btn, y_btn_inicio + (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos
        )

        btn_salir = dibujar_boton(
            pantalla, "SALIR",
            x_btn, y_btn_inicio + 2 * (btn_alto + espacio_v),
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
                nombre_jugador = ""
                rol_elegido = ""
                dificultad = ""
                input_activo = False
                estado = estado_nombre
            elif btn_puntajes.collidepoint(mouse_pos):
                estado = estado_puntajes
            elif btn_salir.collidepoint(mouse_pos):
                corriendo = False


    elif estado == estado_nombre:
        rect_interno = dibujar_marco(pantalla)

        dibujar_texto(
            pantalla, "Registro de Jugador",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 80
        )

        dibujar_texto(
            pantalla, "Ingresa tu nombre:",
            fuente_subt, color_texto2,
            ancho // 2, Y_SUBTITULO_NOMBRE
        )

        color_input = (25, 30, 25)
        pygame.draw.rect(pantalla, color_input, input_rect_nombre)
        borde_color = (220, 210, 160) if input_activo else (120, 120, 100)
        pygame.draw.rect(pantalla, borde_color, input_rect_nombre, 2)

        dibujar_texto(
            pantalla, nombre_jugador,
            fuente_subt, color_texto,
            input_rect_nombre.centerx,                     
            input_rect_nombre.y + input_rect_nombre.height // 2,  
            centro=True
        )

        btn_ancho = 180
        btn_alto = 50
        x_btn = ancho // 2 - btn_ancho // 2
        y_btn = input_rect_nombre.bottom + 30

        btn_siguiente = dibujar_boton(
            pantalla, "SIGUIENTE",
            x_btn, y_btn,
            btn_ancho, btn_alto, mouse_pos
        )

        dibujar_texto(
            pantalla, "ESC para cancelar y volver al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        if mouse_click and btn_siguiente.collidepoint(mouse_pos):
            if nombre_jugador.strip() != "":
                estado = estado_modo

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu

    elif estado == estado_modo:
        rect_interno = dibujar_marco(pantalla)

        dibujar_texto(
            pantalla, f"Hola, {nombre_jugador}",
            fuente_subt, color_texto,
            ancho // 2, rect_interno.top + 70
        )

        dibujar_texto(
            pantalla, "Elige tu personaje",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 120
        )

        separacion = 260
        center_left = ancho // 2 - separacion // 2
        center_right = ancho // 2 + separacion // 2

        y_personajes = rect_interno.top + 170

        rect_jugador = dibujar_personaje_escalado(
            personaje_normal, pantalla, center_left, y_personajes, escala=2.5
        )

        rect_cazador = dibujar_personaje_escalado(
            cazador, pantalla, center_right, y_personajes, escala=2.5
        )

        btn_ancho = 220
        btn_alto = 50

        y_btn = rect_jugador.bottom + 25 

        btn_jugador = dibujar_boton(
            pantalla, "JUGADOR",
            center_left - btn_ancho // 2,
            y_btn,
            btn_ancho, btn_alto, mouse_pos
        )

        btn_cazador = dibujar_boton(
            pantalla, "CAZADOR",
            center_right - btn_ancho // 2,
            y_btn,
            btn_ancho, btn_alto, mouse_pos
        )

        dibujar_texto(
            pantalla, "ESC para cancelar y volver al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        if mouse_click:
            if btn_jugador.collidepoint(mouse_pos):
                rol_elegido = "normal"
                estado = estado_dificultad
            elif btn_cazador.collidepoint(mouse_pos):
                rol_elegido = "cazador"
                estado = estado_dificultad

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu

    elif estado == estado_dificultad:
        rect_interno = dibujar_marco(pantalla)
        dibujar_texto(
            pantalla, "Selecciona la dificultad",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 90
        )

        btn_ancho = 220
        btn_alto = 50
        espacio_v = 18
        x_btn = ancho // 2 - btn_ancho // 2
        y_inicio = rect_interno.top + 160

        btn_facil = dibujar_boton(
            pantalla, "FÁCIL",
            x_btn, y_inicio,
            btn_ancho, btn_alto, mouse_pos
        )
        btn_media = dibujar_boton(
            pantalla, "MEDIA",
            x_btn, y_inicio + (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos
        )
        btn_dificil = dibujar_boton(
            pantalla, "DIFÍCIL",
            x_btn, y_inicio + 2 * (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos
        )

        btn_comenzar = dibujar_boton(
            pantalla, "COMENZAR",
            x_btn, y_inicio + 3 * (btn_alto + espacio_v) + 10,
            btn_ancho, btn_alto, mouse_pos,
            color_base=(110, 46, 32),     
            color_hover=(95, 62, 42),    
            color_borde=(140, 110, 70),    
            color_inner=(40, 26, 18)     
        )


        if dificultad:
            dibujar_texto(
                pantalla, f"Dificultad elegida: {dificultad.upper()}",
                fuente_subt, color_texto2,
                ancho // 2, rect_interno.bottom - 80
            )

        dibujar_texto(
            pantalla, "ESC para cancelar y volver al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        if mouse_click:
            if btn_facil.collidepoint(mouse_pos):
                dificultad = "facil"
            elif btn_media.collidepoint(mouse_pos):
                dificultad = "media"
            elif btn_dificil.collidepoint(mouse_pos):
                dificultad = "dificil"
            elif btn_comenzar.collidepoint(mouse_pos):
                if dificultad:
                    estado = estado_juego

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

        dibujar_texto(
            pantalla, "(Aquí va el top 5)",
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

    elif estado == estado_juego:
        rect_interno = dibujar_marco(pantalla)

        dibujar_texto(
            pantalla, "MAPA DEL LABERINTO",
            fuente_titulo, color_texto,
            ancho // 2, rect_interno.top + 60
        )

        info = f"Jugador: {nombre_jugador}  |  Rol: {rol_elegido.upper()}  |  Dificultad: {dificultad.upper()}"
        dibujar_texto(
            pantalla, info,
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.top + 110
        )

        y_personajes = rect_interno.centery + 40
        if rol_elegido == "cazador":
            cazador(pantalla, ancho // 2 - 120, y_personajes)
            personaje_normal(pantalla, ancho // 2 + 40, y_personajes)
        else:
            personaje_normal(pantalla, ancho // 2 - 120, y_personajes)
            cazador(pantalla, ancho // 2 + 40, y_personajes)

        dibujar_texto(
            pantalla, "Presiona ESC para volver al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu

    pygame.display.flip()

pygame.quit()
exit()
