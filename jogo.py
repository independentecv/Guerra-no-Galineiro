import pygame
from PPlay.collision import Collision
from entities import Enemy, Chicken, Puddle
import random
import config
from entities import Enemy
from entities import Enemy, Chicken
from boss import BossFazendeiro


def novo_jogo():
    return {
        "sementes": config.STARTING_SEEDS,
        "pintinhos": config.MAX_PINTINHOS,
        "rodada": 1,
        "estado": "COMPRA",
        "fila_spawn": [],
        "proximo_spawn": 0,
        "inimigos": [],
        "ovos": [],
        "pocas": [],
        "inventario": {tipo: 0 for tipo in config.ITEM_TYPES},
        "item_para_equipar": None,
        "galinha_selecionada": None,
        "ranking_salvo": False,
        "posicao_ranking": None,
        "carga_pintinho": 0,
        "carga_galo": 0,
        "boss": None,
    }


def matar_inimigo(inimigo, estado_jogo, lista_remocao):
    if inimigo in lista_remocao:
        return

    inimigo.vivo = False
    lista_remocao.append(inimigo)

    estado_jogo["sementes"] += config.ENEMY_DROP[inimigo.tipo]

    estado_jogo["carga_pintinho"] = min(
        100,
        estado_jogo["carga_pintinho"] + 100
    )

    estado_jogo["carga_galo"] = min(
        100,
        estado_jogo["carga_galo"] + 100
    )

    if random.random() < config.ITEM_DROP_CHANCE:
        tipo_item = random.choice(config.ITEM_TYPES)
        estado_jogo["inventario"][tipo_item] += 1

def resetar_partida(ninhos, galinhas):
    for ninho in ninhos:
        ninho["ocupado"] = False
        ninho["galinha"] = None

    galinhas.clear()

    return novo_jogo()

def iniciar_onda(estado_jogo, agora):
    if estado_jogo["rodada"] == 7:
        estado_jogo["fila_spawn"] = []
        estado_jogo["inimigos"] = []
        estado_jogo["boss"] = BossFazendeiro()
    else:
        tipos = config.tipos_disponiveis_na_rodada(estado_jogo["rodada"])

        qtde = config.WAVE_BASE_ENEMIES + (
            estado_jogo["rodada"] - 1
        ) * config.WAVE_ENEMIES_INCREMENT

        estado_jogo["fila_spawn"] = [
            random.choice(tipos) for _ in range(qtde)
        ]

    estado_jogo["proximo_spawn"] = agora
    estado_jogo["estado"] = "ONDA"
def atualizar_boss(estado_jogo):
    boss = estado_jogo["boss"]

    if boss is not None:
        quantidades = [2, 3, 2]

        while boss.ataques_com_spawn < len(boss.ataques_realizados):
            indice = boss.ataques_com_spawn

            if indice < len(quantidades):
                quantidade = quantidades[indice]
                tipos = config.tipos_disponiveis_na_rodada(7)

                for _ in range(quantidade):
                    tipo = random.choice(tipos)
                    estado_jogo["fila_spawn"].append(tipo)

            boss.ataques_com_spawn += 1

        boss.update()

        if boss.derrota_finalizada:
            estado_jogo["boss"] = None
            estado_jogo["estado"] = "COMPRA"
            estado_jogo["sementes"] += config.ROUND_CLEAR_BONUS
            estado_jogo["rodada"] += 1
            estado_jogo["pintinhos"] = min(
                config.MAX_PINTINHOS,
                estado_jogo["pintinhos"] + 1
            )
            return

        if boss.chegou_galinheiro and boss.vivo:
            estado_jogo["boss"] = None
            estado_jogo["estado"] = "GAMEOVER"
def atualizar_spawn(estado_jogo, agora):
    if estado_jogo["fila_spawn"] and agora >= estado_jogo["proximo_spawn"]:
        tipo = estado_jogo["fila_spawn"].pop(0)

        lane = random.randint(0, config.NUM_LANES - 1)

        multiplicador = (
            1.0
            + (estado_jogo["rodada"] - 1)
            * config.WAVE_STAT_MULTIPLIER_PER_ROUND
        )

        estado_jogo["inimigos"].append(
            Enemy(tipo, lane, multiplicador)
        )

        estado_jogo["proximo_spawn"] = (
            agora + config.WAVE_SPAWN_INTERVAL_MS
        )


def atualizar_inimigos(estado_jogo):
    estado_jogo["pocas"] = [
        p for p in estado_jogo["pocas"] if not p.expirou()
    ]

    remocao_ondas = []
    multiplicadores = {}

    agora = pygame.time.get_ticks()

    for poca in estado_jogo["pocas"]:
        poca.update()

    for inimigo in estado_jogo["inimigos"]:
        mult = 1.0

        for poca in estado_jogo["pocas"]:
            if poca.afeta(inimigo):
                mult = min(mult, config.PODRE_SLOW_MULT)

        if agora < getattr(inimigo, "lentidao_pintinho_ate", 0):
            mult = min(mult, 0.5)

        if agora < getattr(inimigo, "congelado_ate", 0):
            mult = 0

        multiplicadores[id(inimigo)] = mult

        if inimigo.hp <= 0:
            matar_inimigo(inimigo, estado_jogo, remocao_ondas)

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


def verificar_fim_onda(estado_jogo):
    if (
        estado_jogo["estado"] == "ONDA"
        and not estado_jogo["fila_spawn"]
        and not estado_jogo["inimigos"]
        and estado_jogo["boss"] is None
    ):
        estado_jogo["estado"] = "COMPRA"
        estado_jogo["sementes"] += config.ROUND_CLEAR_BONUS
        estado_jogo["rodada"] += 1

        estado_jogo["pintinhos"] = min(
            config.MAX_PINTINHOS,
            estado_jogo["pintinhos"] + 1
        )

def tratar_cliques(
    estado_jogo,
    mx,
    my,
    slots_inventario,
    galinhas,
    botoes_upgrade,
    ninhos
):
    clique_tratado = False

    for slot in slots_inventario:
        if (
            slot["x"] <= mx <= slot["x"] + slot["w"]
            and slot["y"] <= my <= slot["y"] + slot["h"]
        ):
            if estado_jogo["inventario"][slot["tipo"]] > 0:
                if estado_jogo["item_para_equipar"] == slot["tipo"]:
                    estado_jogo["item_para_equipar"] = None
                else:
                    estado_jogo["item_para_equipar"] = slot["tipo"]

            clique_tratado = True
            break

    if not clique_tratado and estado_jogo["item_para_equipar"] is not None:
        for galinha in galinhas:
            if galinha.contem_ponto(mx, my):
                tipo = estado_jogo["item_para_equipar"]
                galinha.item_equipado = tipo
                estado_jogo["inventario"][tipo] -= 1
                estado_jogo["item_para_equipar"] = None
                clique_tratado = True
                break

    if not clique_tratado:
        galinha_sel = estado_jogo["galinha_selecionada"]

        if galinha_sel is not None:
            for botao in botoes_upgrade:
                if (
                    botao["x"] <= mx <= botao["x"] + botao["w"]
                    and botao["y"] <= my <= botao["y"] + botao["h"]
                ):
                    custo = galinha_sel.custo_upgrade(botao["stat"])

                    if estado_jogo["sementes"] >= custo:
                        estado_jogo["sementes"] -= custo
                        galinha_sel.aplicar_upgrade(botao["stat"])

                    clique_tratado = True
                    break

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

    if not clique_tratado:
        for ninho in ninhos:
            if ninho["ocupado"]:
                continue

            nx, ny = ninho["x"], ninho["y"]
            nw, nh = ninho["w"], ninho["h"]

            if nx <= mx <= nx + nw and ny <= my <= ny + nh:
                if estado_jogo["sementes"] >= config.CHICKEN_COST:
                    estado_jogo["sementes"] -= config.CHICKEN_COST

                    nova = Chicken(
                        ninho["centro_x"],
                        ninho["centro_y"]
                    )

                    galinhas.append(nova)
                    ninho["ocupado"] = True
                    ninho["galinha"] = nova

                break

def atualizar_galinhas(galinhas, estado_jogo):
    alvos = estado_jogo["inimigos"].copy()

    boss = estado_jogo["boss"]

    if boss is not None and boss.vivo and not boss.atacando:
        alvos.append(boss)

    for galinha in galinhas:
        galinha.update(
            alvos,
            estado_jogo["ovos"]
        )


def atualizar_ovos(estado_jogo, agora):
    ovos_para_remover = []
    remocao_combate = []

    for ovo in estado_jogo["ovos"]:
        ovo.update()
        boss = estado_jogo["boss"]

        if boss is not None and boss.atacando and ovo.alvo is boss:
            ovos_para_remover.append(ovo)
            continue
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

                    distancia = ((ox - hit_x) ** 2 + (oy - hit_y) ** 2) ** 0.5

                    if distancia <= config.GIGANTE_SPLASH_RAIO:
                        outro.hp -= config.GIGANTE_SPLASH_DANO

                        if outro.hp <= 0:
                            matar_inimigo(
                                outro, estado_jogo, remocao_combate
                            )

            elif ovo.tipo_especial == "podre":
                hit_x, hit_y = ovo.centro()

                y_linha = min(
                    range(config.NUM_LANES),
                    key=lambda i: abs(config.lane_y_center(i) - hit_y)
                )
                y_linha = config.lane_y_center(y_linha)

                if y_linha == config.lane_y_center(2):
                    y_linha -= 5

                estado_jogo["pocas"].append(Puddle(hit_x, y_linha))

            elif ovo.tipo_especial == "chupim":
                atingiu.confuso_ate = agora + config.CHUPIM_DURACAO_MS

            if atingiu.hp <= 0:
                matar_inimigo(
                    atingiu, estado_jogo, remocao_combate
                )

        elif estado_jogo["boss"] is not None:
            boss = estado_jogo["boss"]

            if boss.vivo and not boss.atacando and Collision.collided(ovo.sprite, boss.sprite):
                boss.receber_dano(ovo.dano)
                ovos_para_remover.append(ovo)

        elif ovo.fora_da_tela():
            ovos_para_remover.append(ovo)

    for ovo in ovos_para_remover:
        if ovo in estado_jogo["ovos"]:
            estado_jogo["ovos"].remove(ovo)

    for inimigo in remocao_combate:
        if inimigo in estado_jogo["inimigos"]:
            estado_jogo["inimigos"].remove(inimigo)

def resetar_partida(ninhos, galinhas):
    for ninho in ninhos:
        ninho["ocupado"] = False
        ninho["galinha"] = None

    galinhas.clear()

    return novo_jogo()            