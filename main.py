
import pygame

from PPlay.window import Window

import config
import ranking
import interface
import menus
import jogo
import cenario
from especiais_codigo.galo import Galo
from especiais_codigo.pintinho import Pintinho
import especiais_codigo.habilidades as habilidades

cenario.configurar_alturas()

janela = Window(
    config.WINDOW_WIDTH,
    config.WINDOW_HEIGHT,
    config.WINDOW_TITLE
)

galo = Galo()
galo.set_position(450, 250)
pintinho = Pintinho()
pintinho.set_position(450, 350)

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
lane_pintinho = 0

teclas_anteriores = {
    pygame.K_1: False,
    pygame.K_2: False,
    pygame.K_3: False,
    pygame.K_SPACE: False,
    pygame.K_g: False
}

while True:

    agora = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()

    tecla_1 = teclas[pygame.K_1] and not teclas_anteriores[pygame.K_1]
    tecla_2 = teclas[pygame.K_2] and not teclas_anteriores[pygame.K_2]
    tecla_3 = teclas[pygame.K_3] and not teclas_anteriores[pygame.K_3]
    tecla_espaco = teclas[pygame.K_SPACE] and not teclas_anteriores[pygame.K_SPACE]
    tecla_g = teclas[pygame.K_g] and not teclas_anteriores[pygame.K_g]
    for tecla in teclas_anteriores:
        teclas_anteriores[tecla] = teclas[tecla]

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
    if tecla_1:
        lane_pintinho = 0

    if tecla_2:
        lane_pintinho = 1

    if tecla_3:
        lane_pintinho = 2
    if tecla_espaco and estado_jogo["estado"] == "ONDA":
        ativou = habilidades.ativar_pintinho_por_tecla(
            estado_jogo,
            lane_pintinho,
            config.WINDOW_WIDTH - pintinho.sprite.width - 110
        )

        if ativou:
            pintinho.ativar(
                config.WINDOW_WIDTH - pintinho.sprite.width - 110,
                config.lane_y_center(lane_pintinho) - pintinho.sprite.height / 2 - 15
            )

    if tecla_g and estado_jogo["estado"] == "ONDA":
        ativou = habilidades.ativar_galo_por_tecla(estado_jogo)

        if ativou:
            galo.ativar(
            (config.WINDOW_WIDTH - galo.sprite.width) / 2,
            (config.WINDOW_HEIGHT - galo.sprite.height) / 2 - 50
        )
    if estado_jogo["estado"] == "COMPRA":

        if janela.mouse.button_down(1):
            mx, my = janela.mouse.get_position()

            if interface.clicou_em(btn_iniciar, mx, my):
                jogo.iniciar_onda(estado_jogo, agora)

    if estado_jogo["estado"] == "ONDA":

        jogo.atualizar_spawn(estado_jogo, agora)

    jogo.atualizar_inimigos(estado_jogo)
    jogo.atualizar_boss(estado_jogo)

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
    pintinho.update()
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
    if estado_jogo["boss"] is not None:
        estado_jogo["boss"].draw()
    galo.draw()
    pintinho.draw()
    janela.draw_text(
        f"PINTINHO: {estado_jogo['carga_pintinho']}%",
        20, 20, tamanho=18, cor="yellow"
    )

    janela.draw_text(
        f"GALO: {estado_jogo['carga_galo']}%",
        20, 45, tamanho=18, cor="white"
    )
    janela.update()
