
import pygame
from PPlay.sprite import Sprite
import config


def criar_icone(caminho, tamanho=42):
    imagem = pygame.image.load(caminho).convert_alpha()
    area = imagem.get_bounding_rect()
    imagem = imagem.subsurface(area).copy()

    largura, altura = imagem.get_size()
    escala = min(tamanho / largura, tamanho / altura)

    nova_largura = int(largura * escala)
    nova_altura = int(altura * escala)

    imagem = pygame.transform.smoothscale(
        imagem, (nova_largura, nova_altura)
    )

    caminho_temp = caminho.replace(".png", "_redimensionado.png")
    pygame.image.save(imagem, caminho_temp)

    return Sprite(caminho_temp)


def altura_png(caminho):
    return pygame.image.load(caminho).get_height()


def clicou_em(sprite, mx, my):
    return (
        sprite.x <= mx <= sprite.x + sprite.width
        and sprite.y <= my <= sprite.y + sprite.height
    )


def texto_centralizado(janela, texto, y, tamanho=18, cor="white"):
    x = (config.WINDOW_WIDTH - len(texto) * tamanho * 0.5) / 2
    janela.draw_text(texto, x, y, tamanho=tamanho, cor=cor)


def desenhar_botao(janela, botao, texto, mx, my, tamanho=18):
    botao.draw()

    x = botao.x + (botao.width - len(texto) * tamanho * 0.5) / 2
    y = botao.y + (botao.height - tamanho) / 2 - 2

    cor = "white" if clicou_em(botao, mx, my) else "black"
    janela.draw_text(texto, x, y, tamanho=tamanho, cor=cor)

def desenhar_cenario(
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
):
    background.draw()

    for poca in estado_jogo["pocas"]:
        poca.draw()

    if estado_jogo["galinha_selecionada"] is not None:
        estado_jogo["galinha_selecionada"].draw_alcance()

    for galinha in galinhas:
        galinha.draw()

    for inimigo in estado_jogo["inimigos"]:
        inimigo.draw(janela)

    for ovo in estado_jogo["ovos"]:
        ovo.draw()

    painel_topo.draw()

    janela.draw_text(
        f"Onda: {estado_jogo['rodada']}   Sementes: {estado_jogo['sementes']}   "
        f"Pintinhos: {estado_jogo['pintinhos']}/{config.MAX_PINTINHOS}   "
        f"Custo galinha: {config.CHICKEN_COST}",
        10, 15, cor="white"
    )

    if estado_jogo["estado"] == "COMPRA":
        btn_iniciar.draw()

        janela.draw_text(
            "Iniciar Onda",
            btn_iniciar.x + 20,
            btn_iniciar.y + 8,
            cor="black"
        )
    else:
        restantes = (
            len(estado_jogo["fila_spawn"])
            + len(estado_jogo["inimigos"])
        )

        janela.draw_text(
            f"Onda em andamento ({restantes} restantes)",
            btn_iniciar.x - 60,
            btn_iniciar.y + 8,
            cor="white"
        )
        barra_itens.draw()

    for slot in slots_inventario:
        if estado_jogo["item_para_equipar"] == slot["tipo"]:
            slot["sprite_sel"].draw()
        else:
            slot["sprite_normal"].draw()

        slot["icone"].draw()

        qtd = estado_jogo["inventario"][slot["tipo"]]

        janela.draw_text(
            str(qtd),
            slot["x"] + slot["w"] - 16,
            slot["y"] + slot["h"] - 18,
            cor="white"
        )

    if estado_jogo["item_para_equipar"] is not None:
        label = config.ITEM_LABELS[
            estado_jogo["item_para_equipar"]
        ]

        janela.draw_text(
            f"Clique numa galinha para equipar: {label}",
            260,
            barra_itens_y + 22,
            cor="white"
        )

    painel_baixo.draw()

    galinha_sel = estado_jogo["galinha_selecionada"]

    if galinha_sel is None:
        janela.draw_text(
            "Clique numa galinha ja colocada para ver upgrades",
            20,
            painel_baixo_y + 12,
            cor="white"
        )

    else:
        item_txt = (
            config.ITEM_LABELS[galinha_sel.item_equipado]
            if galinha_sel.item_equipado else "nenhum"
        )

        janela.draw_text(
            f"Selecionada -- Dano {galinha_sel.dano} | "
            f"Cooldown {galinha_sel.cooldown_ms}ms | "
            f"Vel. Ovo {int(galinha_sel.vel_ovo)}px/s | "
            f"Item equipado: {item_txt}",
            20,
            painel_baixo_y + 12,
            cor="white"
        )

        for botao in botoes_upgrade:
            custo = galinha_sel.custo_upgrade(botao["stat"])
            pode_pagar = estado_jogo["sementes"] >= custo

            (
                botao["sprite_on"]
                if pode_pagar
                else botao["sprite_off"]
            ).draw()

            janela.draw_text(
                f"{botao['label']}",
                botao["x"] + 15,
                botao["y"] + 6,
                cor="black"
            )

            janela.draw_text(
                f"custo {custo}",
                botao["x"] + 15,
                botao["y"] + 22,
                cor="black"
            )

    janela.draw_text(
        f"FPS: {int(janela.get_fps())}",
        config.WINDOW_WIDTH - 90,
        config.WINDOW_HEIGHT - 20,
        cor="white"
    )
        