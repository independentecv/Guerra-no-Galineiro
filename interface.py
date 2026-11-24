
import pygame
from PPlay.sprite import Sprite
import config
import barra_especial

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
    painel_baixo_y,
    especial_escolhido
):
    nomes_itens = {
        "podre": "PODRE",
        "gigante": "GIGANTE",
        "chupim": "CHUPIM",
        "codorna": "CODORNA"
    }

    efeitos_itens = {
        "podre": "Lentidao",
        "gigante": "Dano",
        "chupim": "Resetar",
        "codorna": "Multiplicar"
    }
    cores_itens = {
    "podre": (166, 217, 106),
    "gigante": (255, 255, 255),
    "chupim": (210, 190, 150),
    "codorna": (214, 166, 232)
}

    tamanhos_itens = {
        "podre": 14,
        "gigante": 18,
        "chupim": 14,
        "codorna": 14
    }
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

    restantes = (
        len(estado_jogo["fila_spawn"])
        + len(estado_jogo["inimigos"])
        + int(
            estado_jogo["boss"] is not None
            and estado_jogo["boss"].vivo
        )
    )

    resumo_topo = [
        (f"Onda: {estado_jogo['rodada']}", 10, "white"),
        (f"Sementes: {estado_jogo['sementes']}", 112, "yellow"),
        (
            f"Custo galinha: {config.custo_galinha(estado_jogo['rodada'])}",
            260,
            "lightgreen"
        ),
        (f"Restantes: {restantes}", 450, "orange"),
        (
            f"Pintinhos: {estado_jogo['pintinhos']}/{config.MAX_PINTINHOS}",
            630,
            "lightblue"
        ),
    ]

    for texto, x, cor in resumo_topo:
        janela.draw_text(texto, x, 15, tamanho=18, cor=cor)

    if estado_jogo["estado"] == "COMPRA":
        btn_iniciar.draw()

    else:
        barra_itens.draw()


    for slot in slots_inventario:
        tipo = slot["tipo"]
        if estado_jogo["item_para_equipar"] == slot["tipo"]:
            slot["sprite_sel"].draw()
        else:
            slot["sprite_normal"].draw()

        

        if tipo == "gigante":
            largura = slot["icone"].width
            altura = slot["icone"].height

            slot["icone"].set_scale(0.65,0.65)

            slot["icone"].set_position(
                slot["x"] + 8,
                slot["y"] + 4
            )
        else:
            slot["icone"].set_position(
                slot["x"] + 8,
                slot["y"] + 8
            )

        slot["icone"].draw()

        qtd = estado_jogo["inventario"][slot["tipo"]]
        
        janela.draw_text(
            str(qtd),
            slot["x"] + 45,
            slot["y"] + slot["h"] - 15,
            cor="white"
        )

        tipo = slot["tipo"]


    painel_baixo.draw()

    galinha_sel = estado_jogo["galinha_selecionada"]

    if galinha_sel is None:
        janela.draw_text(
            "Clique na galinha para aprimorar",
            20,
            painel_baixo_y + 7,
            tamanho=22,
            cor="yellow"
        )

    else:
        item_txt = (
            config.ITEM_LABELS[galinha_sel.item_equipado]
            if galinha_sel.item_equipado else "nenhum"
        )

        for botao in botoes_upgrade:
            custo = galinha_sel.custo_upgrade(botao["stat"])
            pode_pagar = estado_jogo["sementes"] >= custo

            (
                botao["sprite_on"]
                if pode_pagar
                else botao["sprite_off"]
            ).draw()

            if botao["stat"] == "dano":
                valor = str(galinha_sel.dano)

            elif botao["stat"] == "atq":
                valor = f"{galinha_sel.cooldown_ms}ms"

            elif botao["stat"] == "ovo":
                valor = f"{int(galinha_sel.vel_ovo)}px/s"

            janela.draw_text(
                f"{botao['label']}: {valor}",
                botao["x"] + 8,
                botao["y"] + 5,
                tamanho=14,
                cor="black"
            )

            janela.draw_text(
                f"Custo {custo}",
                botao["x"] + 8,
                botao["y"] + 24,
                tamanho=14,
                cor="black"
            )

    
    if especial_escolhido == "PINTINHO":
        if estado_jogo["carga_pintinho"] >= 100:
            piscar = (pygame.time.get_ticks() // 450) % 2 == 0
            if piscar:
                janela.draw_text(
                    "Pintinho: 1/2/3 + ESPAÇO causa dano/lentidão!",
                    600,
                    painel_baixo_y + 7,
                    tamanho=15,
                    cor="yellow"
                )

        barra_especial.desenhar_barra_especial(
            janela,
            "pintinho",
            estado_jogo["carga_pintinho"],
            x=600,
            y=painel_baixo_y + 23
        )

    elif especial_escolhido == "GALO":
        if estado_jogo["carga_galo"] >= 100:
            piscar = (pygame.time.get_ticks() // 450) % 2 == 0
            if piscar:
                janela.draw_text(
                    "Galo: aperte G para paralisar por 2 segundos!",
                    585,
                    painel_baixo_y + 7,
                    tamanho=15,
                    cor="orange"
                )

        barra_especial.desenhar_barra_especial(
            janela,
            "galo",
            estado_jogo["carga_galo"],
            x=600,
            y=painel_baixo_y + 23
        )
    for slot in slots_inventario:
        tipo = slot["tipo"]

        janela.draw_text(
            nomes_itens[tipo].upper(),
            slot["texto_x"],
            slot["y"] + 5,
            tamanho=tamanhos_itens[tipo],
            cor=cores_itens[tipo]
        )

        janela.draw_text(
        f"EFEITO: {efeitos_itens[tipo].upper()}",
        slot["texto_x"],
        slot["y"] + 34,
        tamanho=13,
        cor=cores_itens[tipo]
    )