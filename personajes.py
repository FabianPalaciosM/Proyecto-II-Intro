import pygame

def personaje_x(surface, x, y):
    pygame.draw.rect(surface, (80, 120, 255), (x + 10, y + 20, 20, 25), border_radius=5)  # Cuerpo
    pygame.draw.circle(surface, (255, 220, 190), (x + 20, y + 15), 10)  # Cabeza
    pygame.draw.rect(surface, (80, 200, 120), (x + 10, y + 40, 20, 15))  # Pantalones
    pygame.draw.rect(surface, (0, 0, 0), (x + 12, y + 50, 5, 8))  # Zapato izquierdo
    pygame.draw.rect(surface, (0, 0, 0), (x + 23, y + 50, 5, 8))  # Zapato derecho
    pygame.draw.circle(surface, (0, 0, 0), (x + 16, y + 13), 2)  # Ojo izquierdo
    pygame.draw.circle(surface, (0, 0, 0), (x + 24, y + 13), 2)  # Ojo derecho
    pygame.draw.line(surface, (220, 70, 70), (x + 16, y + 19), (x + 24, y + 19), 2) # Boca
