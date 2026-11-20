import pygame
import random


def aplicar_tremida(intensidade):
    tela = pygame.display.get_surface()

    if tela is None:
        return

    imagem = tela.copy()

    desloc_x = random.randint(-intensidade, intensidade)
    desloc_y = random.randint(-intensidade, intensidade)

    tela.fill((0, 0, 0))

    tela.blit(
        imagem,
        (desloc_x, desloc_y)
    )