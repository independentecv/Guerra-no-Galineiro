
import pygame
from animacoes import carregar_frames_animacao



class Galo:

    def __init__(self):
        self.frames = self._carregar_frames()
        self.indice_frame = 0
        self.sprite = self.frames[0]
        self.duracao = 3000
        self.tempo_ativacao = 0
        self.tempo_frame = 150
        self.proximo_frame = 0
        self.ativo = False

    def _carregar_frames(self):
        caminho = "assets/especiais/galo.png"
        return carregar_frames_animacao(
            caminho,
            quantidade=10,
            escala=0.5,
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
        self.tempo_ativacao = agora
        self.proximo_frame = agora + self.tempo_frame

    def update(self):
        if not self.ativo:
            return

        agora = pygame.time.get_ticks()

        if agora - self.tempo_ativacao >= self.duracao:
            self.ativo = False
            return

        if agora >= self.proximo_frame:
            self.indice_frame = (self.indice_frame + 1) % len(self.frames)

            x = self.sprite.x
            y = self.sprite.y

            self.sprite = self.frames[self.indice_frame]
            self.sprite.set_position(x, y)

            self.proximo_frame = agora + self.tempo_frame

    def draw(self):
        if self.ativo:
            self.sprite.draw()

    def set_position(self, x, y):
        self.sprite.set_position(x, y)
