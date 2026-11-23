
import math
import pygame
from functools import lru_cache
from PPlay.sprite import Sprite


@lru_cache(maxsize=32)
def _carregar_superficies_animacao(
    caminho,
    quantidade,
    escala,
    metodo_escala,
    inverter_horizontal,
):
    spritesheet = pygame.image.load(caminho).convert_alpha()
    largura_frame = spritesheet.get_width() // quantidade
    altura_frame = spritesheet.get_height()
    frames = []

    for i in range(quantidade):
        frame = spritesheet.subsurface(
            (i * largura_frame, 0, largura_frame, altura_frame)
        ).copy()

        if metodo_escala == "scale_by":
            frame = pygame.transform.scale_by(frame, escala)
        else:
            tamanho = (
                max(1, int(largura_frame * escala)),
                max(1, int(altura_frame * escala)),
            )
            if metodo_escala == "smooth":
                frame = pygame.transform.smoothscale(frame, tamanho)
            else:
                frame = pygame.transform.scale(frame, tamanho)

        if inverter_horizontal:
            frame = pygame.transform.flip(frame, True, False)

        frames.append(frame)

    return tuple(frames)


def carregar_frames_animacao(
    caminho,
    quantidade,
    escala=1.0,
    metodo_escala="smooth",
    inverter_horizontal=False,
):
    superficies = _carregar_superficies_animacao(
        caminho,
        quantidade,
        escala,
        metodo_escala,
        inverter_horizontal,
    )
    return [Sprite(superficie) for superficie in superficies]


def calcular_deslocamento(tipo, tempo):
    if tipo == "gato":
        return math.sin(tempo * 12) * 2

    elif tipo == "gaviao":
        return math.sin(tempo * 8) * 3

    elif tipo == "raposa":
        return math.sin(tempo * 10) * 2

    return 0
