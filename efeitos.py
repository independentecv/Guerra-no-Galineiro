import pygame
import random
from PPlay.window import Window


_buffer_tremida = None


def aplicar_tremida(intensidade):
    global _buffer_tremida

    tela = Window.get_screen()

    if tela is None:
        return

    if _buffer_tremida is None or _buffer_tremida.get_size() != tela.get_size():
        _buffer_tremida = pygame.Surface(
            tela.get_size(),
            flags=tela.get_flags(),
            depth=tela.get_bitsize(),
            masks=tela.get_masks(),
        )

    _buffer_tremida.blit(tela, (0, 0))

    desloc_x = random.randint(-intensidade, intensidade)
    desloc_y = random.randint(-intensidade, intensidade)

    tela.fill((0, 0, 0))

    tela.blit(
        _buffer_tremida,
        (desloc_x, desloc_y)
    )