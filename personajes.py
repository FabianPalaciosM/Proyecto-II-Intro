import pygame
from sys import exit

def personaje_normal(surface, x, y):
    piel   = (245, 218, 184)
    pelo   = (20, 20, 20)
    sueter = (70, 100, 160)
    pantal = (40, 50, 90)
    zapato = (25, 25, 30)

    pygame.draw.rect(surface, piel, (x + 10, y + 0, 14, 16))          
    pygame.draw.rect(surface, pelo, (x + 8,  y - 2, 18, 10))          
    pygame.draw.rect(surface, pelo, (x + 8,  y + 2,  4, 14))         
    pygame.draw.rect(surface, piel, (x + 14, y + 16, 6, 3))
    pygame.draw.rect(surface, sueter, (x + 8, y + 19, 18, 16))
    pygame.draw.rect(surface, sueter, (x + 6, y + 20, 5, 13))        
    pygame.draw.rect(surface, piel,   (x + 6, y + 33, 5, 5))          
    pygame.draw.rect(surface, pantal, (x + 10, y + 35, 7, 12))        
    pygame.draw.rect(surface, pantal, (x + 17, y + 35, 7, 12))        
    pygame.draw.rect(surface, zapato, (x + 10, y + 47, 8, 4))
    pygame.draw.rect(surface, zapato, (x + 17, y + 47, 8, 4))

def cazador(surface, x, y):

    piel   = (245, 218, 184)
    pelo   = (10, 10, 10)
    sueter = (90, 30, 40)    
    pantal = (30, 30, 40)
    zapato = (10, 10, 10)

    pygame.draw.rect(surface, piel, (x + 10, y + 0, 14, 16))
    pygame.draw.rect(surface, pelo, (x + 8,  y - 2, 18, 10))
    pygame.draw.rect(surface, pelo, (x + 8,  y + 2,  4, 14))
    pygame.draw.rect(surface, piel, (x + 14, y + 16, 6, 3))
    pygame.draw.rect(surface, sueter, (x + 8, y + 19, 18, 16))
    pygame.draw.rect(surface, sueter, (x + 6, y + 20, 5, 13))
    pygame.draw.rect(surface, piel,   (x + 6, y + 33, 5, 5))
    pygame.draw.rect(surface, pantal, (x + 10, y + 35, 7, 12))
    pygame.draw.rect(surface, pantal, (x + 17, y + 35, 7, 12))
    pygame.draw.rect(surface, zapato, (x + 10, y + 47, 8, 4))
    pygame.draw.rect(surface, zapato, (x + 17, y + 47, 8, 4))

if __name__ == "__main__":
    pygame.init()
    ancho, alto = 500, 300
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Prueba personajes")
    clock = pygame.time.Clock()

    running = True
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        pantalla.fill((70, 90, 110))

        personaje_normal(pantalla, 120, 80)
        cazador(pantalla, 260, 80)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    exit()


