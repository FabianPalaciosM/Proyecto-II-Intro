import pygame
from sys import exit
import os
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
pygame.mixer.init()

pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Escapa del laberinto")
clock = pygame.time.Clock()

fuente_titulo = pygame.font.SysFont("consolas", 52, bold=True)
fuente_subt = pygame.font.SysFont("consolas", 22)
fuente_btn = pygame.font.SysFont("consolas", 26)
fuente_puntaje = pygame.font.SysFont("consolas", 30)
fuente_hud    = pygame.font.SysFont("consolas", 18)

estado_menu  = "menu"
estado_nombre = "nombre"
estado_modo  = "modo"
estado_dificultad  = "dificultad"
estado_puntajes = "puntajes"
estado_juego = "juego"
estado_resultado  = "resultado"

estado = estado_menu

nombre_jugador = ""
input_activo = False
rol_elegido = ""     
dificultad = ""  
modo_puntajes = ""   
energia_max = 100
energia_actual = energia_max

puntaje_final = 0
resultado_gano = False
puntaje_guardado = False
tiempo_partida = 0.0     
enemigos_atrapados = 0      
trampas_activadas = 0     

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
carpeta_sonidos = os.path.join(BASE_DIR, "sonidos")

def ruta_sonido(nombre):
    return os.path.join(carpeta_sonidos, nombre)

try:
    sonido_click    = pygame.mixer.Sound(ruta_sonido("click.wav"))
    sonido_victoria = pygame.mixer.Sound(ruta_sonido("victoria.wav"))
    sonido_derrota  = pygame.mixer.Sound(ruta_sonido("derrota.wav"))

    sonido_click.set_volume(0.4)
    sonido_victoria.set_volume(0.7)
    sonido_derrota.set_volume(0.7)

except (pygame.error, FileNotFoundError):
    # Si algo falla con los archivos de sonido, seguimos sin romper el juego
    print("No se pudieron cargar los sonidos.")
    sonido_click = None
    sonido_victoria = None
    sonido_derrota = None


def reproducir_click():
    if sonido_click:
        sonido_click.play()

def reproducir_victoria():
    if sonido_victoria:
        sonido_victoria.play()

def reproducir_derrota():
    if sonido_derrota:
        sonido_derrota.play()


def musica_menu():
    try:
        pygame.mixer.music.load(ruta_sonido("menu.wav"))  # o .ogg
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except (pygame.error, FileNotFoundError):
        print("⚠ No se pudo cargar la música del menú.")


def musica_juego():
    try:
        pygame.mixer.music.load(ruta_sonido("mapa.wav"))  # o .ogg
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    except (pygame.error, FileNotFoundError):
        print("⚠ No se pudo cargar la música del juego.")

musica_menu()

camino = 0
muro   = 1
liana  = 2
tunel  = 3
trampa = 4
tam_casilla = 18
filas_mapa  = 25
cols_mapa   = 25

matriz_mapa = [[camino for _ in range(cols_mapa)] for _ in range(filas_mapa)]

for c in range(3, 22):
    matriz_mapa[4][c] = muro      
for f in range(6, 18):
    matriz_mapa[f][9] = liana     

for f in range(10, 13):
    for c in range(6, 9):
        matriz_mapa[f][c] = trampa

for f in range(8, 18):
    matriz_mapa[f][18] = tunel
pixel_bg = pygame.Surface((ancho, alto))
tam_cuadro = 16

pixel_bg = pygame.Surface((ancho, alto))
tam_cuadro = 16
for i in range(0, ancho, tam_cuadro):
    for j in range(0, alto, tam_cuadro):
        if (i // tam_cuadro + j // tam_cuadro) % 2 == 0:
            pixel_bg.fill(color_fondo1, (i, j, tam_cuadro, tam_cuadro))
        else:
            pixel_bg.fill(color_fondo2, (i, j, tam_cuadro, tam_cuadro))

input_ancho = 320
input_alto = 40
altura_texto = fuente_subt.get_height()
espacio_texto_input = 15
altura_bloque = altura_texto + espacio_texto_input + input_alto
y_bloque_top = alto // 2 - altura_bloque // 2 - 60
y_subtitulo_nombre = y_bloque_top + altura_texto // 2
y_input_nombre = y_bloque_top + altura_texto + espacio_texto_input
x_input_nombre = ancho // 2 - input_ancho // 2
input_rect_nombre = pygame.Rect(x_input_nombre, y_input_nombre, input_ancho, input_alto)


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

def dibujar_barra_energia(surface, x, y, energia, energia_max):
    if energia_max <= 0:
        ratio = 0
    else:
        ratio = max(0, min(energia / energia_max, 1))


    panel_ancho = 230
    panel_alto = 32
    rect_panel = pygame.Rect(x, y, panel_ancho, panel_alto)

    pygame.draw.rect(surface, (18, 24, 20), rect_panel)       
    pygame.draw.rect(surface, color_btn_b, rect_panel, 2)     
    inner_panel = rect_panel.inflate(-4, -4)
    pygame.draw.rect(surface, color_frame, inner_panel, 2)   

    tile = 3
    amarillo = (240, 220, 120)
    amarillo_osc = (190, 170, 90)

    rayo_cols = 7
    rayo_filas = 8
    rayo_ancho = rayo_cols * tile
    rayo_alto = rayo_filas * tile

    base_x = inner_panel.left + 6
    base_y = inner_panel.top + (inner_panel.height - rayo_alto) // 2

    pixeles_rayo = [
        (2, 0), (3, 0),
        (2, 1), (3, 1), (4, 1),
        (1, 2), (2, 2), (3, 2), (4, 2),
        (2, 3), (3, 3), (4, 3),
        (3, 4), (4, 4), (5, 4),
        (4, 5), (5, 5),
        (5, 6), (6, 6),
        (6, 7),
    ]

    for c, f in pixeles_rayo:
        r = pygame.Rect(base_x + c * tile, base_y + f * tile, tile, tile)
        pygame.draw.rect(surface, amarillo, r)
        pygame.draw.rect(surface, amarillo_osc, r, 1)

    bloques_alto = 8
    num_segmentos = 10
    espacio = 2

    barras_x = base_x + rayo_ancho + 10
    barras_y = inner_panel.centery - bloques_alto // 2

    ancho_disp = inner_panel.right - 8 - barras_x
    ancho_segmento = (ancho_disp - (num_segmentos - 1) * espacio) // num_segmentos
    if ancho_segmento < 4:
        ancho_segmento = 4

    if ratio > 0.6:
        color_seg = (120, 190, 100)   
    elif ratio > 0.3:
        color_seg = (210, 190, 100)   
    else:
        color_seg = (200, 90, 80)  

    segmentos_llenos = int(round(ratio * num_segmentos))

    for i in range(num_segmentos):
        sx = barras_x + i * (ancho_segmento + espacio)
        rect_seg = pygame.Rect(sx, barras_y, ancho_segmento, bloques_alto)

        if i < segmentos_llenos:
            pygame.draw.rect(surface, color_seg, rect_seg)
        else:
            pygame.draw.rect(surface, (30, 36, 32), rect_seg)

        pygame.draw.rect(surface, color_frame, rect_seg, 1)


def estilo_casilla(tipo):
    if tipo == 1: 
        fondo   = (110, 80, 50)
        borde   = (60, 40, 25)
        detalle = (150, 115, 75)
    elif tipo == 2:  
        fondo   = (20, 90, 60)
        borde   = (10, 50, 30)
        detalle = (40, 130, 80)
    elif tipo == 3: 
        fondo   = (25, 30, 35)
        borde   = (10, 15, 18)
        detalle = (60, 70, 80)
    elif tipo == 4:  
        fondo   = (90, 90, 100)
        borde   = (40, 40, 45)
        detalle = (160, 160, 180)
    else:          
        fondo   = (30, 70, 40)
        borde   = (20, 40, 25)
        detalle = (45, 95, 55)

    return fondo, borde, detalle

def dibujar_casilla(surface, x, y, tipo, tam_x, tam_y):
    fondo, borde, detalle = estilo_casilla(tipo)

    r = pygame.Rect(x, y, tam_x, tam_y)

    pygame.draw.rect(surface, fondo, r)
    pygame.draw.rect(surface, borde, r, 1)

    if tipo == 1: 
        pygame.draw.line(surface, detalle,
                         (r.left + 2, r.centery),
                         (r.right - 2, r.centery), 1)
        pygame.draw.line(surface, detalle,
                         (r.centerx, r.top + 2),
                         (r.centerx, r.centery - 2), 1)
        pygame.draw.line(surface, detalle,
                         (r.centerx, r.centery + 2),
                         (r.centerx, r.bottom - 2), 1)

    elif tipo == 2: 
        pygame.draw.rect(surface, detalle,
                         (r.centerx - 2, r.top + 2, 4, r.height - 4))

    elif tipo == 3:  
        inner = r.inflate(-6, -6)
        pygame.draw.rect(surface, detalle, inner, 1)

    elif tipo == 4:
        cx, cy = r.centerx, r.centery
        y_base = r.bottom - 3
        pygame.draw.line(surface, borde,
                         (r.left + 2, y_base),
                         (r.right - 2, y_base), 1)

        num_pinchos = 5
        ancho_pincho = (r.width - 8) // num_pinchos

        for i in range(num_pinchos):
            x1 = r.left + 4 + i * ancho_pincho
            x3 = x1 + ancho_pincho - 2
            x2 = (x1 + x3) // 2 

            y_punta = y_base - (r.height // 2)  

            pygame.draw.polygon(surface, detalle,
                                [(x1, y_base), (x3, y_base), (x2, y_punta)])

    else: 
        p1 = (r.left + 4,  r.centery)
        p2 = (r.centerx,  r.top + 4)
        p3 = (r.right - 4, r.centery)
        p4 = (r.centerx,  r.bottom - 4)
        pygame.draw.polygon(surface, detalle, [p1, p2, p3, p4], 1)

def dibujar_mapa(surface, area_rect, matriz):
    filas = len(matriz)
    cols  = len(matriz[0])

    tam_x = area_rect.width  // cols
    tam_y = area_rect.height // filas

    mapa_ancho = cols  * tam_x
    mapa_alto  = filas * tam_y

    x0 = area_rect.centerx - mapa_ancho // 2
    y0 = area_rect.centery - mapa_alto  // 2

    marco = pygame.Rect(x0 - 8, y0 - 8, mapa_ancho + 16, mapa_alto + 16)
    pygame.draw.rect(surface, (25, 35, 30), marco)
    pygame.draw.rect(surface, color_frame, marco, 3)

    for f in range(filas):
        for c in range(cols):
            tipo = matriz[f][c]
            x = x0 + c * tam_x
            y = y0 + f * tam_y
            dibujar_casilla(surface, x, y, tipo, tam_x, tam_y)


archivo_puntajes = "puntajes.txt" 

def guardar_puntaje(modo, nombre, puntos):
    modo = modo.lower()
    try:
        puntos = int(puntos)
    except ValueError:
        return

    with open(archivo_puntajes, "a", encoding="utf-8") as f:
        f.write(f"{modo};{nombre};{puntos}\n")


def leer_puntajes_top5():
    puntajes = {"escapa": [], "cazador": []}

    if not os.path.exists(archivo_puntajes):
        return puntajes

    with open(archivo_puntajes, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue

            partes = linea.split(";")
            if len(partes) != 3:
                continue

            modo, nombre, puntos = partes
            try:
                puntos = int(puntos)
            except ValueError:
                continue

            modo = modo.lower()
            if modo in puntajes:
                puntajes[modo].append((nombre, puntos))

    for modo in puntajes:
        puntajes[modo].sort(key=lambda x: x[1], reverse=True)
        puntajes[modo] = puntajes[modo][:5]

    return puntajes

def calcular_puntaje(rol, dificultad, energia_restante,
                     tiempo_seg, capturas, trampas):
    dificultad = dificultad.lower()
    if dificultad == "facil":
        mult = 1.0
    elif dificultad == "media":
        mult = 1.3
    elif dificultad == "dificil":
        mult = 1.6
    else:
        mult = 1.0

    energia = max(0, int(energia_restante))
    t = max(1, int(tiempo_seg))          
    caps = max(0, int(capturas))
    trp = max(0, int(trampas))

    puntos_energia = energia * 3
    puntos_capturas = caps * 120       
    penal_tiempo = t * 2
    penal_trampas = trp * 50

    bruto = puntos_energia + puntos_capturas - penal_tiempo - penal_trampas
    bruto = max(0, bruto)
    return int(bruto * mult)

def finalizar_partida(gano):
    global estado, resultado_gano, puntaje_final, puntaje_guardado

    resultado_gano = gano
    puntaje_guardado = False 

    if gano:
        reproducir_victoria()
    else:
        reproducir_derrota()

    puntaje = calcular_puntaje(
        rol_elegido,
        dificultad,
        energia_actual,
        tiempo_partida,
        enemigos_atrapados,
        trampas_activadas
    )

    if gano:
        puntaje += 500
    else:
        puntaje += 100

    puntaje_final = max(0, int(puntaje))
    estado = estado_resultado


corriendo = True
while corriendo:
    dt = clock.tick(fps) / 1000
    mouse_pos = pygame.mouse.get_pos()
    mouse_click = False

    if estado == estado_juego:
        tiempo_partida += dt

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
                reproducir_click()
                nombre_jugador = ""
                rol_elegido = ""
                dificultad = ""
                input_activo = False
                estado = estado_nombre
            elif btn_puntajes.collidepoint(mouse_pos):
                reproducir_click()
                modo_puntajes = ""
                estado = estado_puntajes
            elif btn_salir.collidepoint(mouse_pos):
                reproducir_click()
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
            ancho // 2, y_subtitulo_nombre
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
                reproducir_click()
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
                reproducir_click()
                rol_elegido = "normal"
                estado = estado_dificultad
            elif btn_cazador.collidepoint(mouse_pos):
                reproducir_click()
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

        btn_ancho = 260
        btn_alto = 56
        espacio_v = 24
        x_btn = ancho // 2 - btn_ancho // 2
        y_inicio = rect_interno.top + 160

        btn_facil = dibujar_boton(
            pantalla, "FÁCIL",
            x_btn, y_inicio,
            btn_ancho, btn_alto, mouse_pos,
            color_base=(180, 150, 70),
            color_hover=(200, 170, 90),
            color_borde=(230, 210, 140),
            color_inner=(120, 90, 40)
        )

        btn_media = dibujar_boton(
            pantalla, "MEDIA",
            x_btn, y_inicio + (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos,
            color_base=(175, 110, 60),
            color_hover=(195, 130, 80),
            color_borde=(230, 190, 130),
            color_inner=(120, 70, 35)
        )

        btn_dificil = dibujar_boton(
            pantalla, "DIFÍCIL",
            x_btn, y_inicio + 2 * (btn_alto + espacio_v),
            btn_ancho, btn_alto, mouse_pos,
            color_base=(150, 60, 55),
            color_hover=(175, 80, 70),
            color_borde=(220, 180, 150),
            color_inner=(100, 40, 35)
        )

        dibujar_texto(
            pantalla, "ESC para cancelar y volver al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        if mouse_click:
            if btn_facil.collidepoint(mouse_pos):
                reproducir_click()
                dificultad = "facil"
                musica_juego()
                estado = estado_juego
            elif btn_media.collidepoint(mouse_pos):
                reproducir_click()
                dificultad = "media"
                musica_juego()
                estado = estado_juego
            elif btn_dificil.collidepoint(mouse_pos):
                reproducir_click()
                dificultad = "dificil"
                musica_juego()
                estado = estado_juego

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu
            musica_menu()

    elif estado == estado_puntajes:
        rect_interno = dibujar_marco(pantalla)

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu
            modo_puntajes = "" 

        if modo_puntajes == "":
            dibujar_texto(
                pantalla, "Tabla de puntajes",
                fuente_titulo, color_texto,
                ancho // 2, rect_interno.top + 90
            )
            dibujar_texto(
                pantalla, "Elige un modo",
                fuente_subt, color_texto2,
                ancho // 2, rect_interno.top + 140
            )

            btn_ancho = 260
            btn_alto = 56
            espacio_v = 24
            x_btn = ancho // 2 - btn_ancho // 2

            y_btn_jugador = rect_interno.centery - btn_alto - espacio_v // 2
            y_btn_cazador = rect_interno.centery + espacio_v // 2

            btn_p_jugador = dibujar_boton(
                pantalla, "JUGADOR",
                x_btn, y_btn_jugador,
                btn_ancho, btn_alto, mouse_pos
            )

            btn_p_cazador = dibujar_boton(
                pantalla, "CAZADOR",
                x_btn, y_btn_cazador,
                btn_ancho, btn_alto, mouse_pos
            )

            dibujar_texto(
                pantalla, "ESC para regresar al menú",
                fuente_subt, color_texto2,
                ancho // 2, rect_interno.bottom - 40
            )

            if mouse_click:
                if btn_p_jugador.collidepoint(mouse_pos):
                    reproducir_click()
                    modo_puntajes = "escapa"
                elif btn_p_cazador.collidepoint(mouse_pos):
                    reproducir_click()
                    modo_puntajes = "cazador"
        else:
            puntajes = leer_puntajes_top5()
            lista = puntajes[modo_puntajes]

            titulo_modo = "Top 5 - Jugador" if modo_puntajes == "escapa" else "Top 5 - Cazador"

            dibujar_texto(
                pantalla, titulo_modo,
                fuente_titulo, color_texto,
                ancho // 2, rect_interno.top + 80
            )

            ancho_tabla = int(rect_interno.width * 0.75)
            alto_tabla = 260
            x_tabla = rect_interno.centerx - ancho_tabla // 2
            y_tabla = rect_interno.centery - alto_tabla // 2

            rect_tabla = pygame.Rect(x_tabla, y_tabla, ancho_tabla, alto_tabla)
            pygame.draw.rect(pantalla, (18, 24, 20), rect_tabla)
            pygame.draw.rect(pantalla, color_btn_b, rect_tabla, 3)
            inner = rect_tabla.inflate(-6, -6)
            pygame.draw.rect(pantalla, color_frame, inner, 2)

            x_col_rank  = rect_tabla.left + 40
            x_col_name  = rect_tabla.left + 150
            x_col_score = rect_tabla.right - 60

            y_inicio = rect_tabla.top + 40
            espacio_filas = 38

            if lista:
                for i, (nombre, puntos) in enumerate(lista):
                    y = y_inicio + i * espacio_filas

                    dibujar_texto(
                        pantalla, f"{i+1}.",
                        fuente_puntaje, color_texto,
                        x_col_rank, y, centro=True
                    )

                    dibujar_texto(
                        pantalla, nombre.upper(),
                        fuente_puntaje, color_texto2,
                        x_col_name, y, centro=True
                    )

                    dibujar_texto(
                        pantalla, str(puntos),
                        fuente_puntaje, color_texto,
                        x_col_score, y, centro=True
                    )
            else:
                dibujar_texto(
                    pantalla, "SIN REGISTROS",
                    fuente_puntaje, color_texto2,
                    rect_tabla.centerx, rect_tabla.centery
                )

            dibujar_texto(
                pantalla, "ESC para regresar al menú",
                fuente_subt, color_texto2,
                ancho // 2, rect_interno.bottom - 40
            )

    elif estado == estado_resultado:
        rect_interno = dibujar_marco(pantalla)

        if not puntaje_guardado:
            if rol_elegido == "normal":
                modo = "escapa"
            else:
                modo = "cazador"
            guardar_puntaje(modo, nombre_jugador, puntaje_final)
            puntaje_guardado = True

        if resultado_gano:
            texto_titulo = "¡GANASTE!"
            color_titulo = (200, 220, 140)
        else:
            texto_titulo = "Perdiste..."
            color_titulo = (200, 120, 120)

        dibujar_texto(
            pantalla, texto_titulo,
            fuente_titulo, color_titulo,
            ancho // 2, rect_interno.top + 80
        )

        if rol_elegido == "normal":
            rol_texto = "JUGADOR"
        elif rol_elegido == "cazador":
            rol_texto = "CAZADOR"
        else:
            rol_texto = rol_elegido.upper()

        mapa_dificultad = {
            "facil":   "FÁCIL",
            "media":   "MEDIA",
            "dificil": "DIFÍCIL"
        }
        dif_texto = mapa_dificultad.get(dificultad.lower(), dificultad.upper())

        dibujar_texto(
            pantalla, f"Jugador: {nombre_jugador}",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.top + 150
        )
        dibujar_texto(
            pantalla, f"Rol: {rol_texto}   |   Dificultad: {dif_texto}",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.top + 190
        )
        dibujar_texto(
            pantalla, f"Puntaje: {puntaje_final}",
            fuente_subt, color_texto,
            ancho // 2, rect_interno.top + 230
        )

        btn_ancho = 260
        btn_alto = 56
        espacio_v = 18

        x_btn = ancho // 2 - btn_ancho // 2
        y_btn_inicio = rect_interno.centery

        btn_menu = dibujar_boton(
            pantalla, "VOLVER AL MENÚ",
            x_btn, y_btn_inicio,
            btn_ancho, btn_alto, mouse_pos
        )

        btn_ver_puntajes = dibujar_boton(
            pantalla, "VER PUNTAJES",
            x_btn, y_btn_inicio + btn_alto + espacio_v,
            btn_ancho, btn_alto, mouse_pos
        )

        dibujar_texto(
            pantalla, "ESC para ir al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 40
        )

        if mouse_click:
            if btn_menu.collidepoint(mouse_pos):
                reproducir_click()
                estado = estado_menu
                musica_menu()
            elif btn_ver_puntajes.collidepoint(mouse_pos):
                reproducir_click()
                if rol_elegido == "normal":
                    modo_puntajes = "escapa"
                else:
                    modo_puntajes = "cazador"
                estado = estado_puntajes

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu
            musica_menu()

    elif estado == estado_juego:
        rect_interno = dibujar_marco(pantalla)

        hud_top = rect_interno.top + 12
        panel_ancho = 220

        x_barra = rect_interno.right - 20 - panel_ancho
        y_barra = hud_top
        dibujar_barra_energia(pantalla, x_barra, y_barra, energia_actual, energia_max)

        if rol_elegido == "normal":
            rol_hud = "JUGADOR"
        else:
            rol_hud = "CAZADOR"
        dif_hud = dificultad.upper().replace("FACIL", "FÁCIL")

        texto_info = f"{nombre_jugador}  |  {rol_hud}  |  {dif_hud}"
        info_x = rect_interno.left + 20
        info_y = hud_top + (36 - fuente_hud.get_height()) // 2

        dibujar_texto(
            pantalla, texto_info,
            fuente_hud, color_texto2,
            info_x, info_y, centro=False
        )

        dibujar_mapa(pantalla, rect_interno, matriz_mapa)

        dibujar_texto(
            pantalla, "Presiona ESC para volver al menú",
            fuente_subt, color_texto2,
            ancho // 2, rect_interno.bottom - 30
        )

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            estado = estado_menu
            musica_menu()            


    pygame.display.flip()

if pygame.mixer.get_init():
    pygame.mixer.music.stop()
    pygame.mixer.quit()

pygame.quit()
exit()
