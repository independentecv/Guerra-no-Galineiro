
import config
import ranking
import interface


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

    interface.texto_centralizado(
        janela, "Guerra no Galinheiro",
        config.WINDOW_HEIGHT / 2 - 150,
        tamanho=40, cor="white"
    )

    interface.desenhar_botao(janela, btn_iniciar, "Iniciar", mx, my)
    interface.desenhar_botao(janela, btn_rankings, "Rankings", mx, my)
    interface.desenhar_botao(janela, btn_sair, "Sair", mx, my)

    return acao


def tela_rankings(janela, btn_voltar):
    mx, my = janela.mouse.get_position()
    acao = None

    if janela.mouse.button_down(1):
        if interface.clicou_em(btn_voltar, mx, my):
            acao = "VOLTAR"

    interface.texto_centralizado(
        janela, "Rankings", 90, tamanho=36, cor="white"
    )

    interface.texto_centralizado(
        janela, "Melhores rodadas alcancadas",
        140, tamanho=18, cor="white"
    )

    lista_ranking = ranking.carregar()

    if not lista_ranking:
        interface.texto_centralizado(
            janela, "Nenhuma partida registrada ainda",
            240, tamanho=18, cor="white"
        )
    else:
        for pos, entrada in enumerate(lista_ranking):
            linha = f"{pos + 1:>2}.   Onda {entrada['rodada']:<4}   {entrada['data']}"
            janela.draw_text(
                linha,
                config.WINDOW_WIDTH / 2 - 130,
                200 + pos * 34,
                tamanho=20,
                cor="white"
            )

    interface.desenhar_botao(janela, btn_voltar, "Voltar", mx, my)

    return acao


def tela_gameover(janela, estado_jogo, imagem_gameover,
                  btn_reiniciar, btn_menu, pos_rank):

    mx, my = janela.mouse.get_position()
    acao = None

    if janela.mouse.button_down(1):
        if interface.clicou_em(btn_reiniciar, mx, my):
            acao = "REINICIAR"
        elif interface.clicou_em(btn_menu, mx, my):
            acao = "MENU"

    imagem_gameover.draw()

    interface.texto_centralizado(
        janela,
        f"Onda alcancada: {estado_jogo['rodada']}",
        config.WINDOW_HEIGHT / 2 - 40,
        cor="white"
    )

    if pos_rank is not None:
        interface.texto_centralizado(
            janela,
            f"Posicao no ranking: {pos_rank}o",
            config.WINDOW_HEIGHT / 2 - 12,
            cor="white"
        )

    interface.desenhar_botao(
        janela, btn_reiniciar, "Reiniciar", mx, my
    )

    interface.desenhar_botao(
        janela, btn_menu, "Menu", mx, my
    )

    return acao
