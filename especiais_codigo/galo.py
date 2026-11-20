import pygame
from PPlay.sprite import Sprite


class Galo:

    def __init__(self):
        self.frames = self._carregar_frames()
        self.indice_frame = 0
        self.sprite = self.frames[0]

        self.tempo_frame = 150
        self.proximo_frame = pygame.time.get_ticks() + self.tempo_frame

    def _carregar_frames(self):
        caminho = "assets/especiais/galo.png"

        spritesheet = pygame.image.load(caminho).convert_alpha()

        quantidade = 10
        largura_frame = spritesheet.get_width() // quantidade
        altura_frame = spritesheet.get_height()

        frames = []

        for i in range(quantidade):
            quadro = spritesheet.subsurface(
                (
                    i * largura_frame,
                    0,
                    largura_frame,
                    altura_frame
                )
            ).copy()

            quadro = pygame.transform.smoothscale(
                quadro,
                (
                    int(largura_frame * 0.5),
                    int(altura_frame * 0.5)
                )
            )
            quadro = pygame.transform.flip(quadro, True, False)
            caminho_frame = f"assets/especiais/galo_frame_{i}.png"
            pygame.image.save(quadro, caminho_frame)

            frames.append(Sprite(caminho_frame))

        return frames

    def update(self):
        agora = pygame.time.get_ticks()

        if agora >= self.proximo_frame:
            x = self.sprite.x
            y = self.sprite.y

            self.indice_frame = (
                self.indice_frame + 1
            ) % len(self.frames)

            self.sprite = self.frames[self.indice_frame]
            self.sprite.set_position(x, y)

            self.proximo_frame = agora + self.tempo_frame

    def draw(self):
        self.sprite.draw()

    def set_position(self, x, y):
        self.sprite.set_position(x, y)