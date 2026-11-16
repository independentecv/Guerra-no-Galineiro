
import math
import pygame


def calcular_deslocamento(tipo, tempo):
    if tipo == "gato":
        return math.sin(tempo * 12) * 2

    elif tipo == "gaviao":
        return math.sin(tempo * 8) * 3

    elif tipo == "raposa":
        return math.sin(tempo * 10) * 2

    return 0
