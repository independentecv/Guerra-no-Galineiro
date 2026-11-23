import config
import ranking
import interface
import pygame

imagem_inicial = pygame.image.load("assets/inicial.png")
imagem_ajustada = None
imagem_tela_ranking = None

def menu_principal(janela, btn_iniciar, btn_rankings, btn_sair):
    mx, my = janela.mouse.get_position()
    acao = None

    if janela.mouse.button_down(1):
        if interface.clicou_em(btn_iniciar, mx, my):
            acao = "INICIAR"
        elif interface.clicou_em(btn_rankings, mx, my):
            acao = "RANKINGS"
        elif interface.clicou_em(btn_sair, mx, my):
            acao = "SAIR"

    global imagem_ajustada

    tela = janela.get_screen()

    if imagem_ajustada is None:
        imagem_ajustada = pygame.transform.scale(
            imagem_inicial,
            tela.get_size()
        )

    tela.blit(imagem_ajustada, (0, 0))

    btn_iniciar.draw()
    btn_rankings.draw()
    btn_sair.draw()

    return acao

def tela_rankings(janela, btn_voltar):
    global imagem_tela_ranking

    mx, my = janela.mouse.get_position()
    acao = None

    if janela.mouse.button_down(1):
        if interface.clicou_em(btn_voltar, mx, my):
            acao = "VOLTAR"

    tela = janela.get_screen()
    if imagem_tela_ranking is None:
        imagem_tela_ranking = pygame.image.load(
            "assets/tela_ranking.png"
        ).convert()
        if imagem_tela_ranking.get_size() != tela.get_size():
            imagem_tela_ranking = pygame.transform.smoothscale(
                imagem_tela_ranking, tela.get_size()
            )
    tela.blit(imagem_tela_ranking, (0, 0))

    lista_ranking = ranking.carregar()

    for pos, entrada in enumerate(lista_ranking):
        linha = f"{pos + 1:>2}.   Onda {entrada['rodada']:<4}   {entrada['data']}"
        janela.draw_text(
            linha,
            config.WINDOW_WIDTH / 2 - 130,
            265 + pos * 22,
            tamanho=20,
            cor="white"
        )

    btn_voltar.draw()

    return acao

def tela_gameover(janela, estado_jogo, imagem_gameover,
                  btn_reiniciar, btn_menu):

    mx, my = janela.mouse.get_position()
    acao = None

    if janela.mouse.button_down(1):
        if interface.clicou_em(btn_reiniciar, mx, my):
            acao = "REINICIAR"
        elif interface.clicou_em(btn_menu, mx, my):
            acao = "MENU"

    imagem_gameover.draw()

    btn_reiniciar.draw()
    btn_menu.draw()

    return acao