
import random
import pygame

from PPlay.window import Window
from PPlay.sprite import Sprite
from PPlay.collision import Collision

import interface
import config
import ranking
from entities import Enemy, Chicken, Puddle

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
def _altura_png(caminho):
    return pygame.image.load(caminho).get_height()

config.set_ui_heights(
    _altura_png('assets/painel_topo.png') + _altura_png('assets/barra_itens.png'),
    _altura_png('assets/painel_baixo.png'),
)

janela = Window(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, config.WINDOW_TITLE)
janela.set_background_color((60, 48, 32))   # cor atras da UI, onde nao ha campo

# ============================================================
# CENÁRIO ESTÁTICO (background único)
# ============================================================
imagem_fundo = pygame.image.load('assets/background2.png').convert_alpha()
imagem_fundo = pygame.transform.smoothscale(
    imagem_fundo,
    (config.WINDOW_WIDTH, config.PLAYFIELD_HEIGHT)
)

pygame.image.save(imagem_fundo, 'assets/background2_redimensionado.png')

background = Sprite('assets/background2_redimensionado.png')
background.set_position(0, config.PLAYFIELD_Y)

ninhos = []
for row_index in range(len(config.PLACEMENT_BAND_INDEXES)):
    for slot_index in range(config.SLOTS_PER_ROW):
        centro_x, centro_y = config.placement_slot_position(row_index, slot_index)
        
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

# ============================================================
# UI: barra de topo, barra de itens e painel de upgrade
# ============================================================
painel_topo = Sprite('assets/painel_topo.png')
painel_topo.set_position(0, 0)
TOPO_ALTURA = painel_topo.height

barra_itens = Sprite('assets/barra_itens.png')
barra_itens.set_position(0, TOPO_ALTURA)
BARRA_ITENS_Y = TOPO_ALTURA
BARRA_ITENS_ALTURA = barra_itens.height

painel_baixo = Sprite('assets/painel_baixo.png')
painel_baixo.set_position(0, config.WINDOW_HEIGHT - painel_baixo.height)
gameover = Sprite('assets/gameover.jpg')
gameover.set_scale(
    config.WINDOW_WIDTH / gameover.width,
    config.WINDOW_HEIGHT / gameover.height
)
gameover.set_position(0, 0)
PAINEL_BAIXO_Y = config.WINDOW_HEIGHT - painel_baixo.height

btn_iniciar = Sprite('assets/botao_acao.png')
btn_iniciar.set_position(config.WINDOW_WIDTH - btn_iniciar.width - 15, (TOPO_ALTURA - btn_iniciar.height) / 2)

btn_reiniciar = Sprite('assets/botao_acao.png')
btn_reiniciar.set_position(config.WINDOW_WIDTH / 2 - btn_reiniciar.width / 2, config.WINDOW_HEIGHT / 2 + 30)

btn_menu_gameover = Sprite('assets/botao_acao.png')
btn_menu_gameover.set_position(config.WINDOW_WIDTH / 2 - btn_menu_gameover.width / 2,
                               btn_reiniciar.y + btn_reiniciar.height + 15)

# ============================================================
# MENU PRINCIPAL / RANKINGS
# ============================================================
MENU_GAP = 20
btn_menu_iniciar = Sprite('assets/botao_acao.png')
btn_menu_rankings = Sprite('assets/botao_acao.png')
btn_menu_sair = Sprite('assets/botao_acao.png')
_botoes_menu = [btn_menu_iniciar, btn_menu_rankings, btn_menu_sair]
_menu_y0 = config.WINDOW_HEIGHT / 2 - 30
for _i, _b in enumerate(_botoes_menu):
    _b.set_position(config.WINDOW_WIDTH / 2 - _b.width / 2, _menu_y0 + _i * (_b.height + MENU_GAP))

btn_voltar = Sprite('assets/botao_acao.png')
btn_voltar.set_position(config.WINDOW_WIDTH / 2 - btn_voltar.width / 2, config.WINDOW_HEIGHT - 110)

COR_FUNDO_MENU = (60, 48, 32)


def clicou_em(sprite, mx, my):
    return sprite.x <= mx <= sprite.x + sprite.width and sprite.y <= my <= sprite.y + sprite.height


def texto_centralizado(texto, y, tamanho=18, cor="white"):
    """Centraliza na janela (largura estimada: ~0.5 * tamanho por caractere)."""
    x = (config.WINDOW_WIDTH - len(texto) * tamanho * 0.5) / 2
    janela.draw_text(texto, x, y, tamanho=tamanho, cor=cor)


def desenhar_botao(botao, texto, mx, my, tamanho=18):
    """Desenha o botao com o texto centralizado; o texto fica branco no hover."""
    botao.draw()
    x = botao.x + (botao.width - len(texto) * tamanho * 0.5) / 2
    y = botao.y + (botao.height - tamanho) / 2 - 2
    cor = "white" if clicou_em(botao, mx, my) else "black"
    janela.draw_text(texto, x, y, tamanho=tamanho, cor=cor)

# 3 botões de upgrade, centralizados no painel de baixo
UPGRADES = [("dano", "Dano"), ("atq", "Vel. Ataque"), ("ovo", "Vel. Ovo")]
GAP = 20
LARG_BOTAO = 150
total_largura = len(UPGRADES) * LARG_BOTAO + (len(UPGRADES) - 1) * GAP
x_inicial = (config.WINDOW_WIDTH - total_largura) / 2
y_botoes = PAINEL_BAIXO_Y + 40

botoes_upgrade = []
for i, (stat, label) in enumerate(UPGRADES):
    sprite_on = Sprite('assets/botao_neutro.png')
    sprite_off = Sprite('assets/botao_desabilitado.png')
    x = x_inicial + i * (LARG_BOTAO + GAP)
    sprite_on.set_position(x, y_botoes)
    sprite_off.set_position(x, y_botoes)
    botoes_upgrade.append({"stat": stat, "label": label, "x": x, "y": y_botoes,
                            "w": sprite_on.width, "h": sprite_on.height,
                            "sprite_on": sprite_on, "sprite_off": sprite_off})

# --- slots de inventário (4 itens) ---
ICONE_POR_ITEM = {
    "podre": "assets/icone_podre.png",
    "gigante": "assets/icone_gigante.png",
    "chupim": "assets/icone_chupim.png",
    "codorna": "assets/icone_codorna.png",
}
SLOT_GAP = 15
slots_inventario = []
for i, tipo in enumerate(config.ITEM_TYPES):
    slot_normal = Sprite('assets/slot_normal.png')
    slot_sel = Sprite('assets/slot_selecionado.png')
    icone = criar_icone(ICONE_POR_ITEM[tipo], 80)
    
    x = 15 + i * (slot_normal.width + SLOT_GAP)
    y = BARRA_ITENS_Y + (BARRA_ITENS_ALTURA - slot_normal.height) / 2
    icone.set_position(x, y)
    icone.set_scale(0.5, 0.5)

    slot_normal.set_position(x, y)
    slot_sel.set_position(x, y)

    icone.set_position(
        x + (slot_normal.width - icone.width) / 2 + 15,
        y + (slot_normal.height - icone.height) / 2 +15 
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

def novo_jogo():
    return {
        "sementes": config.STARTING_SEEDS,
        "pintinhos": config.MAX_PINTINHOS,
        "rodada": 1,
        "estado": "COMPRA",          # COMPRA -> ONDA -> COMPRA -> ... ou GAMEOVER
        "fila_spawn": [],
        "proximo_spawn": 0,
        "inimigos": [],
        "ovos": [],
        "pocas": [],
        "inventario": {tipo: 0 for tipo in config.ITEM_TYPES},
        "item_para_equipar": None,
        "galinha_selecionada": None,
        "ranking_salvo": False,      # evita registrar a mesma derrota varias vezes
        "posicao_ranking": None,
    }


def matar_inimigo(inimigo, estado_jogo, lista_remocao):
    """Centraliza o que acontece quando um inimigo morre, não importa a
    causa (ovo normal, respingo do Ovo Gigante, ou dano de entrada da
    poça do Ovo Podre): sementes + chance de item."""
    if inimigo in lista_remocao:
        return
    inimigo.vivo = False
    lista_remocao.append(inimigo)
    estado_jogo["sementes"] += config.ENEMY_DROP[inimigo.tipo]
    if random.random() < config.ITEM_DROP_CHANCE:
        tipo_item = random.choice(config.ITEM_TYPES)
        estado_jogo["inventario"][tipo_item] += 1


galinhas = []


def resetar_partida():
    """Limpa ninhos e galinhas e devolve um estado de jogo novo."""
    for ninho in ninhos:
        ninho["ocupado"] = False
        ninho["galinha"] = None
    galinhas.clear()
    return novo_jogo()


estado_jogo = resetar_partida()
tela = "MENU"          # MENU -> JOGO (e dentro do jogo: COMPRA/ONDA/GAMEOVER) | RANKINGS

while True:
    agora = pygame.time.get_ticks()

    # ============================================================
    # MENU PRINCIPAL
    # ============================================================
    if tela == "MENU":
        mx, my = janela.mouse.get_position()
        if janela.mouse.button_down(1):
            if clicou_em(btn_menu_iniciar, mx, my):
                estado_jogo = resetar_partida()
                tela = "JOGO"
            elif clicou_em(btn_menu_rankings, mx, my):
                tela = "RANKINGS"
            elif clicou_em(btn_menu_sair, mx, my):
                janela.close()
                raise SystemExit

        texto_centralizado("Guerra no Galinheiro", config.WINDOW_HEIGHT / 2 - 150, tamanho=40, cor="white")
        desenhar_botao(btn_menu_iniciar, "Iniciar", mx, my)
        desenhar_botao(btn_menu_rankings, "Rankings", mx, my)
        desenhar_botao(btn_menu_sair, "Sair", mx, my)
        janela.update()
        continue

    # ============================================================
    # RANKINGS
    # ============================================================
    if tela == "RANKINGS":
        mx, my = janela.mouse.get_position()
        if janela.mouse.button_down(1) and clicou_em(btn_voltar, mx, my):
            tela = "MENU"

        texto_centralizado("Rankings", 90, tamanho=36, cor="white")
        texto_centralizado("Melhores rodadas alcancadas", 140, tamanho=18, cor="white")
        lista_ranking = ranking.carregar()
        if not lista_ranking:
            texto_centralizado("Nenhuma partida registrada ainda", 240, tamanho=18, cor="white")
        else:
            for pos, entrada in enumerate(lista_ranking):
                linha = f"{pos + 1:>2}.   Onda {entrada['rodada']:<4}   {entrada['data']}"
                janela.draw_text(linha, config.WINDOW_WIDTH / 2 - 130, 200 + pos * 34, tamanho=20, cor="white")
        desenhar_botao(btn_voltar, "Voltar", mx, my)
        janela.update()
        continue

    # ============================================================
    # GAME OVER
    # ============================================================
    if estado_jogo["estado"] == "GAMEOVER":
        if not estado_jogo["ranking_salvo"]:
            estado_jogo["posicao_ranking"] = ranking.registrar(estado_jogo["rodada"])
            estado_jogo["ranking_salvo"] = True

        mx, my = janela.mouse.get_position()

        if janela.mouse.button_down(1):
            if clicou_em(btn_reiniciar, mx, my):
                estado_jogo = resetar_partida()
            elif clicou_em(btn_menu_gameover, mx, my):
                tela = "MENU"

        gameover.draw()

        texto_centralizado(
            f"Onda alcancada: {estado_jogo['rodada']}",
            config.WINDOW_HEIGHT / 2 - 40,
            cor="white"
        )

        pos_rank = estado_jogo["posicao_ranking"]
        if pos_rank is not None:
            texto_centralizado(
                f"Posicao no ranking: {pos_rank}o",
                config.WINDOW_HEIGHT / 2 - 12,
                cor="white"
            )

        desenhar_botao(btn_reiniciar, "Reiniciar", mx, my)
        desenhar_botao(btn_menu_gameover, "Menu", mx, my)

        janela.update()
        continue

    # ============================================================
    # FASE DE COMPRA: botão de iniciar onda
    # ============================================================
    if estado_jogo["estado"] == "COMPRA":
        if janela.mouse.button_down(1):
            mx, my = janela.mouse.get_position()
            bx, by = btn_iniciar.x, btn_iniciar.y
            if bx <= mx <= bx + btn_iniciar.width and by <= my <= by + btn_iniciar.height:
                tipos = config.tipos_disponiveis_na_rodada(estado_jogo["rodada"])
                qtde = config.WAVE_BASE_ENEMIES + (estado_jogo["rodada"] - 1) * config.WAVE_ENEMIES_INCREMENT
                estado_jogo["fila_spawn"] = [random.choice(tipos) for _ in range(qtde)]
                estado_jogo["proximo_spawn"] = agora
                estado_jogo["estado"] = "ONDA"

    # ============================================================
    # FASE DE ONDA: spawn dos inimigos da fila
    # ============================================================
    if estado_jogo["estado"] == "ONDA":
        if estado_jogo["fila_spawn"] and agora >= estado_jogo["proximo_spawn"]:
            tipo = estado_jogo["fila_spawn"].pop(0)
            lane = random.randint(0, config.NUM_LANES - 1)
            multiplicador = 1.0 + (estado_jogo["rodada"] - 1) * config.WAVE_STAT_MULTIPLIER_PER_ROUND
            estado_jogo["inimigos"].append(Enemy(tipo, lane, multiplicador))
            estado_jogo["proximo_spawn"] = agora + config.WAVE_SPAWN_INTERVAL_MS

    # ============================================================
    # POÇAS (Ovo Podre): expiram, e afetam quem estiver dentro
    # ============================================================
    estado_jogo["pocas"] = [p for p in estado_jogo["pocas"] if not p.expirou()]

    remocao_ondas = []
    multiplicadores = {}
    for inimigo in estado_jogo["inimigos"]:
        mult = 1.0
        for poca in estado_jogo["pocas"]:
            if poca.afeta(inimigo):  # também aplica o dano de entrada, uma vez por inimigo
                mult = min(mult, config.PODRE_SLOW_MULT)
        multiplicadores[id(inimigo)] = mult
        if inimigo.hp <= 0:
            matar_inimigo(inimigo, estado_jogo, remocao_ondas)

    # movimento dos inimigos que sobraram vivos 
    for inimigo in estado_jogo["inimigos"]:
        if inimigo in remocao_ondas:
            continue
        inimigo.update(multiplicadores.get(id(inimigo), 1.0))
        if inimigo.chegou_no_galinheiro():
            inimigo.vivo = False
            remocao_ondas.append(inimigo)
            estado_jogo["pintinhos"] -= 1
            if estado_jogo["pintinhos"] <= 0:
                estado_jogo["estado"] = "GAMEOVER"

    for inimigo in remocao_ondas:
        if inimigo in estado_jogo["inimigos"]:
            estado_jogo["inimigos"].remove(inimigo)

    # onda terminou? (fila vazia + nenhum inimigo restante) 
    if (estado_jogo["estado"] == "ONDA" and not estado_jogo["fila_spawn"]
            and not estado_jogo["inimigos"]):
        estado_jogo["estado"] = "COMPRA"
        estado_jogo["sementes"] += config.ROUND_CLEAR_BONUS
        estado_jogo["rodada"] += 1
        estado_jogo["pintinhos"] = min(config.MAX_PINTINHOS, estado_jogo["pintinhos"] + 1)

    # ============================================================
    # CLIQUE DO MOUSE
    # ordem: item do inventário > equipar em galinha > upgrade >
    #        selecionar galinha > comprar galinha num ninho vazio
    # ============================================================
    if estado_jogo["estado"] != "GAMEOVER" and janela.mouse.button_down(1):
        mx, my = janela.mouse.get_position()
        clique_tratado = False

        # 1) ícone do inventário -> arma/desarma esse item pra equipar
        for slot in slots_inventario:
            if slot["x"] <= mx <= slot["x"] + slot["w"] and slot["y"] <= my <= slot["y"] + slot["h"]:
                if estado_jogo["inventario"][slot["tipo"]] > 0:
                    if estado_jogo["item_para_equipar"] == slot["tipo"]:
                        estado_jogo["item_para_equipar"] = None
                    else:
                        estado_jogo["item_para_equipar"] = slot["tipo"]
                clique_tratado = True
                break

        # 2) se há item armado, clique numa galinha equipa nela
        if not clique_tratado and estado_jogo["item_para_equipar"] is not None:
            for galinha in galinhas:
                if galinha.contem_ponto(mx, my):
                    tipo = estado_jogo["item_para_equipar"]
                    galinha.item_equipado = tipo
                    estado_jogo["inventario"][tipo] -= 1
                    estado_jogo["item_para_equipar"] = None
                    clique_tratado = True
                    break

        # 3) botões de upgrade (só se houver galinha selecionada)
        if not clique_tratado:
            galinha_sel = estado_jogo["galinha_selecionada"]
            if galinha_sel is not None:
                for botao in botoes_upgrade:
                    if botao["x"] <= mx <= botao["x"] + botao["w"] and botao["y"] <= my <= botao["y"] + botao["h"]:
                        custo = galinha_sel.custo_upgrade(botao["stat"])
                        if estado_jogo["sementes"] >= custo:
                            estado_jogo["sementes"] -= custo
                            galinha_sel.aplicar_upgrade(botao["stat"])
                        clique_tratado = True
                        break

        # 4) galinha já colocada -> seleciona/deseleciona
        if not clique_tratado:
            for galinha in galinhas:
                if galinha.contem_ponto(mx, my):
                    if estado_jogo["galinha_selecionada"] is galinha:
                        galinha.selecionada = False
                        estado_jogo["galinha_selecionada"] = None
                    else:
                        if estado_jogo["galinha_selecionada"] is not None:
                            estado_jogo["galinha_selecionada"].selecionada = False
                        galinha.selecionada = True
                        estado_jogo["galinha_selecionada"] = galinha
                    clique_tratado = True
                    break

        # 5) ninho vazio -> comprar galinha nova
        if not clique_tratado:
            for ninho in ninhos:
                if ninho["ocupado"]:
                    continue
                nx, ny = ninho["x"], ninho["y"]
                nw, nh = ninho["w"], ninho["h"]
                if nx <= mx <= nx + nw and ny <= my <= ny + nh:
                    if estado_jogo["sementes"] >= config.CHICKEN_COST:
                        estado_jogo["sementes"] -= config.CHICKEN_COST
                        nova = Chicken(ninho["centro_x"], ninho["centro_y"])
                        galinhas.append(nova)
                        ninho["ocupado"] = True
                        ninho["galinha"] = nova
                    clique_tratado = True
                    break

    # ============================================================
    # ATAQUE DAS GALINHAS
    # ============================================================
    for galinha in galinhas:
        galinha.update(estado_jogo["inimigos"], estado_jogo["ovos"])

    # ============================================================
    # MOVIMENTO/COLISÃO DOS OVOS + EFEITOS DOS ITENS ESPECIAIS
    # ============================================================
    ovos_para_remover = []
    remocao_combate = []
    for ovo in estado_jogo["ovos"]:
        ovo.update()

        atingiu = None
        for inimigo in estado_jogo["inimigos"]:
            if inimigo in remocao_combate:
                continue
            if Collision.collided(ovo.sprite, inimigo.sprite):
                atingiu = inimigo
                break

        if atingiu is not None:
            atingiu.hp -= ovo.dano
            ovos_para_remover.append(ovo)

            if ovo.tipo_especial == "gigante":
                hit_x = atingiu.sprite.x + atingiu.sprite.width / 2
                hit_y = atingiu.sprite.y + atingiu.sprite.height / 2
                for outro in estado_jogo["inimigos"]:
                    if outro is atingiu or outro in remocao_combate:
                        continue
                    ox = outro.sprite.x + outro.sprite.width / 2
                    oy = outro.sprite.y + outro.sprite.height / 2
                    if ((ox - hit_x) ** 2 + (oy - hit_y) ** 2) ** 0.5 <= config.GIGANTE_SPLASH_RAIO:
                        outro.hp -= config.GIGANTE_SPLASH_DANO
                        if outro.hp <= 0:
                            matar_inimigo(outro, estado_jogo, remocao_combate)
            elif ovo.tipo_especial == "podre":
                hit_x, hit_y = ovo.centro()
                estado_jogo["pocas"].append(Puddle(hit_x, hit_y))
            elif ovo.tipo_especial == "chupim":
                atingiu.confuso_ate = agora + config.CHUPIM_DURACAO_MS

            if atingiu.hp <= 0:
                matar_inimigo(atingiu, estado_jogo, remocao_combate)

        elif ovo.fora_da_tela():
            ovos_para_remover.append(ovo)

    for ovo in ovos_para_remover:
        estado_jogo["ovos"].remove(ovo)
    for inimigo in remocao_combate:
        if inimigo in estado_jogo["inimigos"]:
            estado_jogo["inimigos"].remove(inimigo)

    # ============================================================
    # DESENHO
    # ============================================================
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

    # barra de topo
    painel_topo.draw()
    janela.draw_text(
        f"Onda: {estado_jogo['rodada']}   Sementes: {estado_jogo['sementes']}   "
        f"Pintinhos: {estado_jogo['pintinhos']}/{config.MAX_PINTINHOS}   "
        f"Custo galinha: {config.CHICKEN_COST}",
        10, 15, cor="white",
    )
    if estado_jogo["estado"] == "COMPRA":
        btn_iniciar.draw()
        janela.draw_text("Iniciar Onda", btn_iniciar.x + 20, btn_iniciar.y + 8, cor="black")
    else:
        restantes = len(estado_jogo["fila_spawn"]) + len(estado_jogo["inimigos"])
        janela.draw_text(f"Onda em andamento ({restantes} restantes)", btn_iniciar.x - 60, btn_iniciar.y + 8, cor="white")

    # barra de itens (inventário) 
    barra_itens.draw()
    for slot in slots_inventario:
        if estado_jogo["item_para_equipar"] == slot["tipo"]:
            slot["sprite_sel"].draw()
        else:
            slot["sprite_normal"].draw()
        slot["icone"].draw()
        qtd = estado_jogo["inventario"][slot["tipo"]]
        janela.draw_text(str(qtd), slot["x"] + slot["w"] - 16, slot["y"] + slot["h"] - 18, cor="white")
    if estado_jogo["item_para_equipar"] is not None:
        label = config.ITEM_LABELS[estado_jogo["item_para_equipar"]]
        janela.draw_text(f"Clique numa galinha para equipar: {label}", 260, BARRA_ITENS_Y + 22, cor="white")

    # painel de baixo (upgrade)
    painel_baixo.draw()
    galinha_sel = estado_jogo["galinha_selecionada"]
    if galinha_sel is None:
        janela.draw_text("Clique numa galinha ja colocada para ver upgrades", 20, PAINEL_BAIXO_Y + 12, cor="white")
    else:
        item_txt = config.ITEM_LABELS[galinha_sel.item_equipado] if galinha_sel.item_equipado else "nenhum"
        janela.draw_text(
            f"Selecionada -- Dano {galinha_sel.dano} | Cooldown {galinha_sel.cooldown_ms}ms | "
            f"Vel. Ovo {int(galinha_sel.vel_ovo)}px/s | Item equipado: {item_txt}",
            20, PAINEL_BAIXO_Y + 12, cor="white",
        )
        for botao in botoes_upgrade:
            custo = galinha_sel.custo_upgrade(botao["stat"])
            pode_pagar = estado_jogo["sementes"] >= custo
            (botao["sprite_on"] if pode_pagar else botao["sprite_off"]).draw()
            janela.draw_text(f"{botao['label']}", botao["x"] + 15, botao["y"] + 6, cor="black")
            janela.draw_text(f"custo {custo}", botao["x"] + 15, botao["y"] + 22, cor="black")

    janela.draw_text(f"FPS: {int(janela.get_fps())}", config.WINDOW_WIDTH - 90, config.WINDOW_HEIGHT - 20, cor="white")

    janela.update()
