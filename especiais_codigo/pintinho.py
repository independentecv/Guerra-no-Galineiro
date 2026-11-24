
import pygame
from animacoes import carregar_frames_animacao


class Pintinho:

    def __init__(self):
        self.frames = self._carregar_frames()
        self.indice_frame = 0
        self.sprite = self.frames[0]
        self.tempo_frame = 130
        self.proximo_frame = 0
        self.ativo = False

    def _carregar_frames(self):
        caminho = "assets/especiais/pintinho.png"
        return carregar_frames_animacao(
            caminho,
            quantidade=14,
            escala=0.85,
            inverter_horizontal=True,
        )

    def ativar(self, x, y):
        if self.ativo:
            return

        self.ativo = True
        self.indice_frame = 0
        self.sprite = self.frames[0]
        self.sprite.set_position(x, y)

        agora = pygame.time.get_ticks()
        self.proximo_frame = agora + self.tempo_frame

    def update(self):
        if not self.ativo:
            return False

        agora = pygame.time.get_ticks()

        if agora < self.proximo_frame:
            return False

        if self.indice_frame + 1 >= len(self.frames):
            self.ativo = False
            return True

        self.indice_frame += 1

        x = self.sprite.x
        y = self.sprite.y

        self.sprite = self.frames[self.indice_frame]
        self.sprite.set_position(x, y)

        self.proximo_frame = agora + self.tempo_frame
        return False

    def draw(self):
        if self.ativo:
            self.sprite.draw()

    def set_position(self, x, y):
        self.sprite.set_position(x, y)
