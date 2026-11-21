import pygame

pygame.mixer.init()

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
import efeitos
import barra_especial

cenario.configurar_alturas()

MUSICA_NORMAL = "sounds/fundo.mp3"
MUSICA_CHEFE = "sounds/fundo_chefe.mp3"

pygame.mixer.music.load(MUSICA_NORMAL)
pygame.mixer.music.set_volume(0.5)


musica_atual = "normal"

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
gameover_chefe = elementos["gameover_chefe"]
escolha = elementos["escolha"]

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
especial_escolhido = None
lane_pintinho = 0

teclas_anteriores = {
    pygame.K_1: False,
    pygame.K_2: False,
    pygame.K_3: False,
    pygame.K_SPACE: False,
    pygame.K_g: False
}

rodada_anterior = None
estado_anterior = None
boss_anterior = False

tremida_ate = 0
DURACAO_TREMIDA = 1000
INTENSIDADE_TREMIDA = 16

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
            tela = "ESCOLHA"

            if musica_atual != "normal":
                pygame.mixer.music.load(MUSICA_NORMAL)
                pygame.mixer.music.play(-1)
                musica_atual = "normal"

        elif acao == "RANKINGS":
            tela = "RANKINGS"

        elif acao == "SAIR":
            pygame.mixer.music.stop()
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

    if tela == "ESCOLHA":

        escolha.draw()

        mx, my = janela.mouse.get_position()

        if janela.mouse.button_down(1):

            if mx < config.WINDOW_WIDTH / 2:
                especial_escolhido = "PINTINHO"

                estado_jogo = jogo.resetar_partida(
                    ninhos,
                    galinhas
                )

                pygame.mixer.music.load(MUSICA_NORMAL)
                pygame.mixer.music.play(-1)
                musica_atual = "normal"
                tela = "JOGO"

            else:
                especial_escolhido = "GALO"

                estado_jogo = jogo.resetar_partida(
                    ninhos,
                    galinhas
                )

                pygame.mixer.music.load(MUSICA_NORMAL)
                pygame.mixer.music.play(-1)
                musica_atual = "normal"
                tela = "JOGO"

        janela.update()
        continue
    if estado_jogo["estado"] == "GAMEOVER":

        musica_gameover = (
            "gameover_chefe"
            if estado_jogo["gameover_chefe"]
            else "gameover"
        )

        if musica_atual != musica_gameover:
            pygame.mixer.music.load(
                f"sounds/{musica_gameover}.mp3"
            )
            pygame.mixer.music.play(0)
            musica_atual = musica_gameover

        imagem_final = (
            gameover_chefe
            if estado_jogo["gameover_chefe"]
            else gameover
        )

        acao = menus.tela_gameover(
            janela,
            estado_jogo,
            imagem_final,
            btn_reiniciar,
            btn_menu_gameover,
        )

        if acao == "REINICIAR":
            estado_jogo = jogo.resetar_partida(ninhos, galinhas)

            if musica_atual != "normal":
                pygame.mixer.music.load(MUSICA_NORMAL)
                pygame.mixer.music.play(-1)
                musica_atual = "normal"

        elif acao == "MENU":
            tela = "MENU"

        janela.update()
        continue

    if especial_escolhido == "PINTINHO":

        if tecla_1:
            lane_pintinho = 0

        if tecla_2:
            lane_pintinho = 1

        if tecla_3:
            lane_pintinho = 2

    if (
        especial_escolhido == "PINTINHO"
        and tecla_espaco
        and estado_jogo["estado"] == "ONDA"
    ):

        ativou = habilidades.ativar_pintinho_por_tecla(
            estado_jogo,
            lane_pintinho,
            config.WINDOW_WIDTH - pintinho.sprite.width - 110
        )

        if ativou:
            pintinho.ativar(
                config.WINDOW_WIDTH - pintinho.sprite.width - 110,
                config.lane_y_center(lane_pintinho)
                - pintinho.sprite.height / 2
                - 15
            )

    if (
        especial_escolhido == "GALO"
        and tecla_g
        and estado_jogo["estado"] == "ONDA"
    ):

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

    agora = pygame.time.get_ticks()

    boss_atual = estado_jogo["boss"] is not None

    rodada_chefe = (
        estado_jogo["rodada"] == estado_jogo["proxima_rodada_chefe"]
    )

    if rodada_anterior is not None:

        if (
            rodada_anterior != estado_jogo["rodada"]
            and rodada_chefe
            and estado_jogo["estado"] == "COMPRA"
        ):
            tremida_ate = agora + DURACAO_TREMIDA

        elif (
            rodada_chefe
            and estado_anterior == "COMPRA"
            and estado_jogo["estado"] == "ONDA"
        ):
            tremida_ate = agora + DURACAO_TREMIDA

        elif (
            boss_anterior
            and not boss_atual
            and estado_jogo["estado"] == "COMPRA"
        ):
            tremida_ate = agora + DURACAO_TREMIDA

    rodada_anterior = estado_jogo["rodada"]
    estado_anterior = estado_jogo["estado"]
    boss_anterior = boss_atual

    if rodada_chefe:

        if musica_atual != "chefe":
            pygame.mixer.music.load(MUSICA_CHEFE)
            pygame.mixer.music.play(-1)
            musica_atual = "chefe"

    else:

        if musica_atual != "normal":
            pygame.mixer.music.load(MUSICA_NORMAL)
            pygame.mixer.music.play(-1)
            musica_atual = "normal"

    if especial_escolhido == "GALO":
        galo.update()

    if especial_escolhido == "PINTINHO":
        pintinho.update()

    if rodada_chefe:

        if estado_jogo["estado"] == "COMPRA":
            background_atual = elementos["background_medio"]
        else:
            background_atual = elementos["background_escuro"]

    else:
        background_atual = elementos["background"]

    interface.desenhar_cenario(
        janela,
        background_atual,
        estado_jogo,
        galinhas,
        painel_topo,
        btn_iniciar,
        barra_itens,
        slots_inventario,
        painel_baixo,
        botoes_upgrade,
        barra_itens_y,
        painel_baixo_y,
         especial_escolhido
    )

    if estado_jogo["boss"] is not None:
        estado_jogo["boss"].draw()

    if especial_escolhido == "GALO":
        galo.draw()
    if especial_escolhido == "PINTINHO":
        pintinho.draw()
    

    agora = pygame.time.get_ticks()

    if agora < tremida_ate:

        restante = tremida_ate - agora

        intensidade = max(
            1,
            int(
                INTENSIDADE_TREMIDA
                * restante
                / DURACAO_TREMIDA
            )
        )

        efeitos.aplicar_tremida(intensidade)

    janela.update()

    if pygame.time.get_ticks() < tremida_ate:
        efeitos.aplicar_tremida(8)
        pygame.display.flip()