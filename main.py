
import pygame

from PPlay.window import Window

import config
import ranking
import interface
import menus
import jogo
import cenario
from especiais_codigo.galo import Galo

cenario.configurar_alturas()

janela = Window(
    config.WINDOW_WIDTH,
    config.WINDOW_HEIGHT,
    config.WINDOW_TITLE
)

galo = Galo()
galo.set_position(450, 250)

elementos = cenario.criar_cenario()
barra_itens_y = elementos["barra_itens_y"]
painel_baixo_y = elementos["painel_baixo_y"]

janela.set_background_color(elementos["cor_fundo_menu"])

background = elementos["background"]
ninhos = elementos["ninhos"]

painel_topo = elementos["painel_topo"]
barra_itens = elementos["barra_itens"]
painel_baixo = elementos["painel_baixo"]
gameover = elementos["gameover"]

btn_iniciar = elementos["btn_iniciar"]
btn_reiniciar = elementos["btn_reiniciar"]
btn_menu_gameover = elementos["btn_menu_gameover"]

btn_menu_iniciar = elementos["btn_menu_iniciar"]
btn_menu_rankings = elementos["btn_menu_rankings"]
btn_menu_sair = elementos["btn_menu_sair"]
btn_voltar = elementos["btn_voltar"]

botoes_upgrade = elementos["botoes_upgrade"]
slots_inventario = elementos["slots_inventario"]

galinhas = []
estado_jogo = jogo.resetar_partida(ninhos, galinhas)

tela = "MENU"


while True:

    agora = pygame.time.get_ticks()

    if tela == "MENU":

        acao = menus.menu_principal(
            janela,
            btn_menu_iniciar,
            btn_menu_rankings,
            btn_menu_sair
        )

        if acao == "INICIAR":
            estado_jogo = jogo.resetar_partida(ninhos, galinhas)
            tela = "JOGO"

        elif acao == "RANKINGS":
            tela = "RANKINGS"

        elif acao == "SAIR":
            janela.close()
            raise SystemExit

        janela.update()
        continue

    if tela == "RANKINGS":

        acao = menus.tela_rankings(
            janela,
            btn_voltar
        )

        if acao == "VOLTAR":
            tela = "MENU"

        janela.update()
        continue

    if estado_jogo["estado"] == "GAMEOVER":

        if not estado_jogo["ranking_salvo"]:
            estado_jogo["posicao_ranking"] = ranking.registrar(
                estado_jogo["rodada"]
            )

            estado_jogo["ranking_salvo"] = True

        acao = menus.tela_gameover(
            janela,
            estado_jogo,
            gameover,
            btn_reiniciar,
            btn_menu_gameover,
            estado_jogo["posicao_ranking"]
        )

        if acao == "REINICIAR":
            estado_jogo = jogo.resetar_partida(ninhos, galinhas)

        elif acao == "MENU":
            tela = "MENU"

        janela.update()
        continue

    if estado_jogo["estado"] == "COMPRA":

        if janela.mouse.button_down(1):
            mx, my = janela.mouse.get_position()

            if interface.clicou_em(btn_iniciar, mx, my):
                jogo.iniciar_onda(estado_jogo, agora)

    if estado_jogo["estado"] == "ONDA":

        jogo.atualizar_spawn(estado_jogo, agora)

    jogo.atualizar_inimigos(estado_jogo)

    jogo.verificar_fim_onda(estado_jogo)

    if (
        estado_jogo["estado"] != "GAMEOVER"
        and janela.mouse.button_down(1)
    ):

        mx, my = janela.mouse.get_position()

        jogo.tratar_cliques(
            estado_jogo,
            mx,
            my,
            slots_inventario,
            galinhas,
            botoes_upgrade,
            ninhos
        )

    jogo.atualizar_galinhas(
        galinhas,
        estado_jogo
    )

    jogo.atualizar_ovos(
        estado_jogo,
        agora
    )
    galo.update()
    interface.desenhar_cenario(
        janela,
        background,
        estado_jogo,
        galinhas,
        painel_topo,
        btn_iniciar,
        barra_itens,
        slots_inventario,
        painel_baixo,
        botoes_upgrade,
        barra_itens_y,
        painel_baixo_y
    )
    galo.draw()
    janela.update()
