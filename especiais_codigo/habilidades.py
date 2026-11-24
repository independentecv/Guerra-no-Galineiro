
import pygame
import config

som_galo = pygame.mixer.Sound("sounds/galo.mp3")
som_pintinho = pygame.mixer.Sound("sounds/pintinho.mp3")
som_pintinho_1 = pygame.mixer.Sound("sounds/pintinho.mp3")
som_pintinho_2 = pygame.mixer.Sound("sounds/pintinho2.mp3")

proximo_som_pintinho = 0
DANO_MAX_PINTINHO = 35
DANO_MIN_PINTINHO = 15
DISTANCIA_MAX_PINTINHO = 800

MULT_PINTINHO = config.PINTINHO_MULT_VELOCIDADE


def ativar_lentidao_pintinho(estado_jogo, lane):
    estado_jogo["lentidao_pintinho_lane"] = lane
    for inimigo in estado_jogo["inimigos"]:
        if inimigo.vivo and inimigo.lane_atual == lane:
            inimigo.lentidao_pintinho_ativa = True


def remover_lentidao_pintinho(estado_jogo):
    estado_jogo["lentidao_pintinho_lane"] = None
    for inimigo in estado_jogo["inimigos"]:
        inimigo.lentidao_pintinho_ativa = False


def tocar_som_pintinho():
    global proximo_som_pintinho

    if proximo_som_pintinho == 0:
        som_pintinho_1.play()
        proximo_som_pintinho = 1
    else:
        som_pintinho_2.play()
        proximo_som_pintinho = 0
def ativar_pintinho(estado_jogo, lane, x_pintinho):
    for inimigo in estado_jogo["inimigos"]:

        if inimigo.lane_atual != lane:
            continue

        distancia = abs(inimigo.sprite.x - x_pintinho)

        if distancia >= DISTANCIA_MAX_PINTINHO:
            dano = DANO_MIN_PINTINHO
        else:
            proporcao = distancia / DISTANCIA_MAX_PINTINHO

            dano = DANO_MAX_PINTINHO - (
                DANO_MAX_PINTINHO - DANO_MIN_PINTINHO
            ) * proporcao

        if not inimigo.vivo:
            continue

        inimigo.hp -= int(dano)


def ativar_pintinho_por_tecla(estado_jogo):
    if estado_jogo["carga_pintinho"] < 100:
        return False

    estado_jogo["carga_pintinho"] = 0
    tocar_som_pintinho()
    return True


DURACAO_CONGELAMENTO_GALO = 2000



def ativar_galo(estado_jogo):
    agora = pygame.time.get_ticks()

    for inimigo in estado_jogo["inimigos"]:
        if not inimigo.vivo:
            continue

        inimigo.congelado_ate = (
            agora + DURACAO_CONGELAMENTO_GALO
        )


def ativar_galo_por_tecla(estado_jogo):
    if estado_jogo["carga_galo"] < 100:
        return False

    if not estado_jogo["inimigos"]:
        return False

    ativar_galo(estado_jogo)

    estado_jogo["carga_galo"] = 0
    som_galo.play()
    return True