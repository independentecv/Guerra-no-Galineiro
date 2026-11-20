
import pygame
from PPlay.sprite import Sprite

import config
import interface


def configurar_alturas():
    config.set_ui_heights(
        interface.altura_png('assets/painel_topo.png')
        + interface.altura_png('assets/barra_itens.png'),
        interface.altura_png('assets/painel_baixo.png')
    )


def criar_cenario():
    def criar_background(caminho, destino):
        imagem = pygame.image.load(caminho).convert_alpha()

        imagem = pygame.transform.smoothscale(
            imagem,
            (config.WINDOW_WIDTH, config.PLAYFIELD_HEIGHT)
        )

        pygame.image.save(imagem, destino)

        background = Sprite(destino)
        background.set_position(0, config.PLAYFIELD_Y)

        return background


    background = criar_background(
        'assets/background2.png',
        'assets/background_normal_redimensionado.png'
    )

    background_medio = criar_background(
        'assets/mapa_medio.png',
        'assets/mapa_medio_redimensionado.png'
    )

    background_escuro = criar_background(
        'assets/mapa_escuro.png',
        'assets/mapa_escuro_redimensionado.png'
    )

    ninhos = []

    for row_index in range(len(config.PLACEMENT_BAND_INDEXES)):
        for slot_index in range(config.SLOTS_PER_ROW):
            centro_x, centro_y = config.placement_slot_position(
                row_index, slot_index
            )

            w_ninho = 64
            h_ninho = 48

            x_ninho = centro_x - w_ninho / 2
            y_ninho = centro_y - h_ninho / 2

            ninhos.append({
                "x": x_ninho,
                "y": y_ninho,
                "w": w_ninho,
                "h": h_ninho,
                "centro_x": centro_x,
                "centro_y": centro_y,
                "ocupado": False,
                "galinha": None
            })

    painel_topo = Sprite('assets/painel_topo.png')
    painel_topo.set_position(0, 0)

    topo_altura = painel_topo.height

    barra_itens = Sprite('assets/barra_itens.png')
    barra_itens.set_position(0, topo_altura)

    barra_itens_y = topo_altura
    barra_itens_altura = barra_itens.height

    painel_baixo = Sprite('assets/painel_baixo.png')
    painel_baixo.set_position(
        0,
        config.WINDOW_HEIGHT - painel_baixo.height
    )

    painel_baixo_y = config.WINDOW_HEIGHT - painel_baixo.height

    gameover = Sprite('assets/gameover.jpg')
    gameover.set_scale(
        config.WINDOW_WIDTH / gameover.width,
        config.WINDOW_HEIGHT / gameover.height
    )
    gameover.set_position(0, 0)

    btn_iniciar = Sprite('assets/botao_acao.png')
    btn_iniciar.set_position(
        config.WINDOW_WIDTH - btn_iniciar.width - 15,
        (topo_altura - btn_iniciar.height) / 2
    )

    btn_reiniciar = Sprite('assets/botao_acao.png')
    btn_reiniciar.set_position(
        config.WINDOW_WIDTH / 2 - btn_reiniciar.width / 2,
        config.WINDOW_HEIGHT / 2 + 30
    )

    btn_menu_gameover = Sprite('assets/botao_acao.png')
    btn_menu_gameover.set_position(
        config.WINDOW_WIDTH / 2 - btn_menu_gameover.width / 2,
        btn_reiniciar.y + btn_reiniciar.height + 15
    )

    menu_gap = 20

    btn_menu_iniciar = Sprite('assets/botao_acao.png')
    btn_menu_rankings = Sprite('assets/botao_acao.png')
    btn_menu_sair = Sprite('assets/botao_acao.png')

    botoes_menu = [
        btn_menu_iniciar,
        btn_menu_rankings,
        btn_menu_sair
    ]

    menu_y0 = config.WINDOW_HEIGHT / 2 - 30

    for i, botao in enumerate(botoes_menu):
        botao.set_position(
            config.WINDOW_WIDTH / 2 - botao.width / 2,
            menu_y0 + i * (botao.height + menu_gap)
        )

    btn_voltar = Sprite('assets/botao_acao.png')
    btn_voltar.set_position(
        config.WINDOW_WIDTH / 2 - btn_voltar.width / 2,
        config.WINDOW_HEIGHT - 110
    )

    upgrades = [
        ("dano", "Dano"),
        ("atq", "Vel. Ataque"),
        ("ovo", "Vel. Ovo")
    ]

    gap = 20
    larg_botao = 150

    total_largura = (
        len(upgrades) * larg_botao
        + (len(upgrades) - 1) * gap
    )

    x_inicial = (config.WINDOW_WIDTH - total_largura) / 2
    y_botoes = painel_baixo_y + 40

    botoes_upgrade = []

    for i, (stat, label) in enumerate(upgrades):
        sprite_on = Sprite('assets/botao_neutro.png')
        sprite_off = Sprite('assets/botao_desabilitado.png')

        x = x_inicial + i * (larg_botao + gap)

        sprite_on.set_position(x, y_botoes)
        sprite_off.set_position(x, y_botoes)

        botoes_upgrade.append({
            "stat": stat,
            "label": label,
            "x": x,
            "y": y_botoes,
            "w": sprite_on.width,
            "h": sprite_on.height,
            "sprite_on": sprite_on,
            "sprite_off": sprite_off
        })

    icone_por_item = {
        "podre": "assets/icone_podre.png",
        "gigante": "assets/icone_gigante.png",
        "chupim": "assets/icone_chupim.png",
        "codorna": "assets/icone_codorna.png"
    }

    slot_gap = 15
    slots_inventario = []

    for i, tipo in enumerate(config.ITEM_TYPES):
        slot_normal = Sprite('assets/slot_normal.png')
        slot_sel = Sprite('assets/slot_selecionado.png')

        icone = interface.criar_icone(
            icone_por_item[tipo], 80
        )

        x = 15 + i * (slot_normal.width + slot_gap)

        y = barra_itens_y + (
            barra_itens_altura - slot_normal.height
        ) / 2

        icone.set_position(x, y)
        icone.set_scale(0.5, 0.5)

        slot_normal.set_position(x, y)
        slot_sel.set_position(x, y)

        icone.set_position(
            x + (slot_normal.width - icone.width) / 2 + 15,
            y + (slot_normal.height - icone.height) / 2 + 15
        )

        slots_inventario.append({
            "tipo": tipo,
            "x": x,
            "y": y,
            "w": slot_normal.width,
            "h": slot_normal.height,
            "sprite_normal": slot_normal,
            "sprite_sel": slot_sel,
            "icone": icone
        })

    return {
        "background": background,
        "background_medio": background_medio,
        "background_escuro": background_escuro,
        "ninhos": ninhos,
        "painel_topo": painel_topo,
        "barra_itens": barra_itens,
        "painel_baixo": painel_baixo,
        "gameover": gameover,
        "btn_iniciar": btn_iniciar,
        "btn_reiniciar": btn_reiniciar,
        "btn_menu_gameover": btn_menu_gameover,
        "btn_menu_iniciar": btn_menu_iniciar,
        "btn_menu_rankings": btn_menu_rankings,
        "btn_menu_sair": btn_menu_sair,
        "btn_voltar": btn_voltar,
        "botoes_upgrade": botoes_upgrade,
        "slots_inventario": slots_inventario,
        "barra_itens_y": barra_itens_y,
        "painel_baixo_y": painel_baixo_y,
        "cor_fundo_menu": (60, 48, 32)
    }
