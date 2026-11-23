import pygame
from PPlay.window import Window
from animacoes import carregar_frames_animacao
import config



class BossFazendeiro:
    def __init__(self, aparicao=1):
        self.som_ataque = pygame.mixer.Sound("sounds/chefe_ataque.mp3")
        self.som_derrota = pygame.mixer.Sound("sounds/chefe_derrota.mp3")

        self.frames = carregar_frames_animacao(
            "assets/animacoes/boss/fazendeiro.png",
            quantidade=8,
            escala=0.7,
            metodo_escala="scale_by",
        )
        self.frames_ataque = carregar_frames_animacao(
            "assets/animacoes/boss/fazendeiro_ataque.png",
            quantidade=12,
            escala=0.7,
            metodo_escala="scale_by",
        )
        self.frames_derrota = carregar_frames_animacao(
            "assets/animacoes/boss/fazendeiro_derrota.png",
            quantidade=16,
            escala=0.7,
            metodo_escala="scale_by",
        )

        self.derrotado = False
        self.indice_derrota = 0
        self.tempo_frame_derrota = 100
        self.proximo_frame_derrota = 0
        self.ataques_com_spawn = 0
        self.derrota_finalizada = False

        self.indice_frame = 0
        self.tempo_frame = 120
        self.proximo_frame = pygame.time.get_ticks() + self.tempo_frame

        self.lane = 1
        self.sprite = self.frames[0]
        self.atacando = False
        self.indice_ataque = 0
        self.tempo_frame_ataque = 100
        self.proximo_frame_ataque = 0

        self.marcos_ataque = [75, 50, 25]
        self.ataques_realizados = []

        self.x = -self.sprite.width
        self.y = config.lane_y_center(self.lane) - self.sprite.height / 2

        self.aparicao = aparicao
        self.vida_maxima = int(650 * (1 + 0.95 * (aparicao - 1)))
        self.vida = self.vida_maxima

        self.vivo = True
        self.velocidade = 45
        self.ultimo_update = pygame.time.get_ticks()

        self.sprite.set_position(self.x, self.y)
        self.chegou_galinheiro = False

    def receber_dano(self, dano):
        if not self.vivo or self.atacando:
            return

        self.vida -= dano

        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.derrotado = True
            self.som_derrota.play()
            self.indice_derrota = 0
            self.proximo_frame_derrota = pygame.time.get_ticks()

            self.sprite = self.frames_derrota[0]
            self.sprite.set_position(self.x, self.y)
            return

        porcentagem = (self.vida / self.vida_maxima) * 100

        for marco in self.marcos_ataque:
            if porcentagem <= marco and marco not in self.ataques_realizados:
                self.ataques_realizados.append(marco)
                self.iniciar_ataque()
                break

    def iniciar_ataque(self):
        self.atacando = True
        self.som_ataque.play()
        self.indice_ataque = 0

        agora = pygame.time.get_ticks()
        self.proximo_frame_ataque = agora
        self.ultimo_update = agora

        self.sprite = self.frames_ataque[0]
        self.sprite.set_position(self.x, self.y)

    def desenhar_vida(self):
        janela = Window.get_screen()

        largura = 100
        altura = 10

        x = self.x + (self.sprite.width - largura) / 2
        y = self.y - 20

        proporcao = self.vida / self.vida_maxima

        pygame.draw.rect(janela, (80, 0, 0), (x, y, largura, altura))
        pygame.draw.rect(
            janela,
            (0, 220, 0),
            (x, y, largura * proporcao, altura)
        )

    def update(self):
        agora = pygame.time.get_ticks()

        if self.derrotado:
            if agora >= self.proximo_frame_derrota:
                self.indice_derrota += 1

                if self.indice_derrota >= len(self.frames_derrota):
                    self.derrota_finalizada = True
                    return

                self.sprite = self.frames_derrota[self.indice_derrota]
                self.sprite.set_position(self.x, self.y)

                self.proximo_frame_derrota = agora + self.tempo_frame_derrota

            return

        if self.atacando:
            self.ultimo_update = agora

            if agora >= self.proximo_frame_ataque:
                self.indice_ataque += 1

                if self.indice_ataque >= len(self.frames_ataque):
                    self.atacando = False
                    self.indice_frame = 0
                    self.sprite = self.frames[0]
                    self.ultimo_update = agora
                else:
                    self.sprite = self.frames_ataque[self.indice_ataque]

                self.proximo_frame_ataque = agora + self.tempo_frame_ataque

            self.sprite.set_position(self.x, self.y)
            return

        delta = (agora - self.ultimo_update) / 1000
        self.ultimo_update = agora

        self.x += self.velocidade * delta

        if agora >= self.proximo_frame:
            self.indice_frame = (self.indice_frame + 1) % len(self.frames)
            self.sprite = self.frames[self.indice_frame]
            self.proximo_frame = agora + self.tempo_frame

        self.sprite.set_position(self.x, self.y)

        if self.x + self.sprite.width >= config.GALINHEIRO_X:
            self.chegou_galinheiro = True

    def draw(self):
        if not self.derrota_finalizada:
            self.sprite.draw()

            if not self.derrotado:
                self.desenhar_vida()