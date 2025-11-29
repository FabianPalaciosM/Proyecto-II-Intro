import pygame
from sys import exit

def personaje_normal(surface, x, y):
    #E: El mapa, la x e y donde se crea
    #S: El aspecto del jugador
    #Crea el aspecto del jugador
    piel   = (245, 218, 184)
    pelo   = (20, 20, 20)
    sueter = (70, 100, 160)
    pantal = (40, 50, 90)
    zapato = (25, 25, 30)

    escala = 0.6

    pygame.draw.rect(surface, piel, (x + 10*escala, y + 0*escala, 14*escala, 16*escala))
    pygame.draw.rect(surface, pelo, (x + 8*escala,  y - 2*escala, 18*escala, 10*escala))
    pygame.draw.rect(surface, pelo, (x + 8*escala,  y + 2*escala,  4*escala, 14*escala))
    pygame.draw.rect(surface, piel, (x + 14*escala, y + 16*escala, 6*escala, 3*escala))
    pygame.draw.rect(surface, sueter, (x + 8*escala, y + 19*escala, 18*escala, 16*escala))
    pygame.draw.rect(surface, sueter, (x + 6*escala, y + 20*escala, 5*escala, 13*escala))
    pygame.draw.rect(surface, piel,   (x + 6*escala, y + 33*escala, 5*escala, 5*escala))
    pygame.draw.rect(surface, pantal, (x + 10*escala, y + 35*escala, 7*escala, 12*escala))
    pygame.draw.rect(surface, pantal, (x + 17*escala, y + 35*escala, 7*escala, 12*escala))
    pygame.draw.rect(surface, zapato, (x + 10*escala, y + 47*escala, 8*escala, 4*escala))
    pygame.draw.rect(surface, zapato, (x + 17*escala, y + 47*escala, 8*escala, 4*escala))

def cazador(surface, x, y):
    #E: El mapa, la x e y donde se crea
    #S: El aspecto del enemigo
    #Crea el aspecto del enemigo
    piel   = (245, 218, 184)
    pelo   = (10, 10, 10)
    sueter = (90, 30, 40)
    pantal = (30, 30, 40)
    zapato = (10, 10, 10)

    escala = 0.6

    pygame.draw.rect(surface, piel, (x + 10*escala, y + 0*escala, 14*escala, 16*escala))
    pygame.draw.rect(surface, pelo, (x + 8*escala,  y - 2*escala, 18*escala, 10*escala))
    pygame.draw.rect(surface, pelo, (x + 8*escala,  y + 2*escala,  4*escala, 14*escala))
    pygame.draw.rect(surface, piel, (x + 14*escala, y + 16*escala, 6*escala, 3*escala))
    pygame.draw.rect(surface, sueter, (x + 8*escala, y + 19*escala, 18*escala, 16*escala))
    pygame.draw.rect(surface, sueter, (x + 6*escala, y + 20*escala, 5*escala, 13*escala))
    pygame.draw.rect(surface, piel,   (x + 6*escala, y + 33*escala, 5*escala, 5*escala))
    pygame.draw.rect(surface, pantal, (x + 10*escala, y + 35*escala, 7*escala, 12*escala))
    pygame.draw.rect(surface, pantal, (x + 17*escala, y + 35*escala, 7*escala, 12*escala))
    pygame.draw.rect(surface, zapato, (x + 10*escala, y + 47*escala, 8*escala, 4*escala))
    pygame.draw.rect(surface, zapato, (x + 17*escala, y + 47*escala, 8*escala, 4*escala))

