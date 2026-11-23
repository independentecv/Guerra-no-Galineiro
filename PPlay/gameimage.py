import pygame
from .gameobject import GameObject
from .window import Window

"""
===============================================================================
POWER PPLAY 2.0 - Framework de Alta Performance para Desenvolvimento de Jogos
===============================================================================
Desenvolvedor Líder e Arquiteto da Versão 2.0: 
    Kauã Neves Jesus de Paula

Ano de Lançamento: 2026
Instituição: Universidade Federal Fluminense (IC-UFF) - Niterói, RJ
-------------------------------------------------------------------------------
Este software é uma evolução profunda e modernização da biblioteca PPlay,
originalmente concebida pela Equipe PPlay:
    Prof. Esteban Clua, Prof. Anselmo Montenegro, Gabriel Saldanha,
    Adônis Gasiglia, Yuri Nogueira e Sergio Herman.
===============================================================================
"""

class GameImage(GameObject):
    """
    GameImage cuida de carregar, armazenar e desenhar imagens na tela.
    Inclui um sistema de cache para evitar carregamentos redundantes do disco.
    """
    
    # Nosso "Almoxarifado" de imagens (Cache)
    # Chave: nome do arquivo, Valor: superfície do pygame carregada
    _resource_cache = {}

    def __init__(self, caminho_imagem):
        super().__init__()
        
        if isinstance(caminho_imagem, pygame.Surface):
            self.image = caminho_imagem
        elif caminho_imagem in GameImage._resource_cache:
            self.image = GameImage._resource_cache[caminho_imagem]
        else:
            # Se não estiver lá, carrega do disco e otimiza
            try:
                # convert_alpha() faz o blit ser até 5x mais rápido
                self.image = pygame.image.load(caminho_imagem).convert_alpha()
                # Guarda no cache para o próximo objeto que pedir
                GameImage._resource_cache[caminho_imagem] = self.image
            except pygame.error:
                print(f"ERRO: Não foi possível carregar a imagem: {caminho_imagem}")
                # Cria uma superfície rosa choque temporária para não crashar o jogo
                self.image = pygame.Surface((32, 32))
                self.image.fill((255, 0, 255))

        # Define as dimensões do GameObject baseadas na imagem
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # Rect interno para operações do Pygame
        self.rect = self.image.get_rect()
        self._draw_cache_key = None
        self._draw_cache = None

    def _render_surface(self, source, source_key):
        if (
            self.scale_x == 1.0
            and self.scale_y == 1.0
            and self.rotation == 0
            and self.transparency == 255
            and source.get_alpha() in (None, 255)
        ):
            return source

        cache_key = (
            source_key,
            self.width,
            self.height,
            self.scale_x,
            self.scale_y,
            self.rotation,
            self.transparency,
        )

        if cache_key != self._draw_cache_key:
            imagem = source.copy()
            imagem.set_alpha(self.transparency)

            if self.rotation != 0:
                imagem = pygame.transform.rotate(imagem, self.rotation)

            if self.scale_x != 1.0 or self.scale_y != 1.0:
                nova_w = max(1, int(self.width * self.scale_x))
                nova_h = max(1, int(self.height * self.scale_y))
                imagem = pygame.transform.scale(imagem, (nova_w, nova_h))

            self._draw_cache_key = cache_key
            self._draw_cache = imagem

        return self._draw_cache

    def draw(self):
        """Desenha a imagem na tela aplicando escala, rotação e transparência."""
        self.rect.x = self.x
        self.rect.y = self.y
        imagem = self._render_surface(self.image, (id(self.image),))
        Window.get_screen().blit(imagem, self.rect)

    def draw_collision_box(self, cor=(0, 255, 0)):
        """Método de Debug: Desenha a caixa de colisão do objeto."""
        pygame.draw.rect(Window.get_screen(), cor, (self.x, self.y, self.width, self.height), 1)

    @classmethod
    def get_cache_size(cls):
        """Retorna quantas imagens únicas estão carregadas na memória."""
        return len(cls._resource_cache)