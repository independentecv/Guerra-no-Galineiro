
import pygame

IMAGENS = {}
ANIMACOES = {}

QUANTIDADE_QUADROS = 8
DURACAO_QUADRO = 100


def carregar_imagem(nome):
    if nome not in IMAGENS:
        caminho = f"assets/especiais/{nome}.png"
        IMAGENS[nome] = pygame.image.load(caminho).convert_alpha()

    return IMAGENS[nome]


def carregar_animacao(especial):
    if especial not in ANIMACOES:
        caminho = f"assets/animacoes/{especial}/{especial} 100.png"

        spritesheet = pygame.image.load(caminho).convert_alpha()

        largura_quadro = spritesheet.get_width() // QUANTIDADE_QUADROS
        altura_quadro = spritesheet.get_height()

        quadros = []

        for i in range(QUANTIDADE_QUADROS):
            quadro = spritesheet.subsurface(
                (i * largura_quadro, 0, largura_quadro, altura_quadro)
            ).copy()

            quadros.append(quadro)

        ANIMACOES[especial] = quadros

    return ANIMACOES[especial]


def desenhar_barra_especial(janela, especial, carga, x=550, y=500):

    carga = max(0, min(100, int(carga)))

    if carga >= 100:
        quadros = carregar_animacao(especial)

        agora = pygame.time.get_ticks()
        indice = (agora // DURACAO_QUADRO) % QUANTIDADE_QUADROS

        imagem = quadros[indice]

    else:
        nivel = (carga // 25) * 25
        nome = f"{especial} {nivel}"
        imagem = carregar_imagem(nome)
    imagem = pygame.transform.scale(
        imagem,
        (int(imagem.get_width() * 2.0), int(imagem.get_height() * 2.0))
    )
    janela.get_screen().blit(imagem, (x, y))