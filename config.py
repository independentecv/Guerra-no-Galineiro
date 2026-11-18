# --- oiii nilo
WINDOW_WIDTH = 960
WINDOW_TITLE = "Guerra no Galinheiro"

PLAYFIELD_HEIGHT = 600
TOP_UI_HEIGHT = 0        # preenchido por set_ui_heights()
BOTTOM_UI_HEIGHT = 0     # preenchido por set_ui_heights()
PLAYFIELD_Y = 0          # y onde o campo comeca, msm coisa que altura da UI do topo
WINDOW_HEIGHT = PLAYFIELD_HEIGHT


def set_ui_heights(top, bottom):
    """Chame UMA vez, antes de criar a Window, com a altura (px) da UI do
    topo (painel_topo + barra_itens) e da UI de baixo (painel_baixo)."""
    global TOP_UI_HEIGHT, BOTTOM_UI_HEIGHT, PLAYFIELD_Y, WINDOW_HEIGHT
    TOP_UI_HEIGHT = int(top)
    BOTTOM_UI_HEIGHT = int(bottom)
    PLAYFIELD_Y = TOP_UI_HEIGHT
    WINDOW_HEIGHT = TOP_UI_HEIGHT + PLAYFIELD_HEIGHT + BOTTOM_UI_HEIGHT

# --- Zonas laterais ---
FOREST_WIDTH = 140          # floresta: spawn dos inimigos (esquerda)
GALINHEIRO_WIDTH = 140      # galinheiro: base a defender (direita)

PLAYFIELD_X = FOREST_WIDTH
PLAYFIELD_WIDTH = WINDOW_WIDTH - FOREST_WIDTH - GALINHEIRO_WIDTH
GALINHEIRO_X = WINDOW_WIDTH - GALINHEIRO_WIDTH

# --- Faixas horizontais do campo (5 no total) ---
# Ordem de cima para baixo: Linha 1 (ataque) / Fileira 1 (galinhas) /
# Linha 2 (ataque) / Fileira 2 (galinhas) / Linha 3 (ataque)
NUM_BANDS = 5
BAND_HEIGHT = PLAYFIELD_HEIGHT // NUM_BANDS

LANE_BAND_INDEXES = [0, 2, 4]         # bandas que são linhas de ataque
PLACEMENT_BAND_INDEXES = [1, 3]       # bandas que são fileiras de galinhas

# --- Espaços de posicionamento das galinhas ---
SLOTS_PER_ROW = 5
NEST_WIDTH = 96
NEST_HEIGHT = 64

# Gato: mais rápido, menos HP, anda sempre na mesma linha.
# Gavião: mais lento, mais HP (tanque), anda sempre na mesma linha.
# Raposa: velocidade/HP intermediários, pode pular entre as 3 linhas.
ENEMY_STATS = {
    "gato": {
        "velocidade": "alta",
        "hp": "baixo",
        "pula_linha": False,
    },
    "gaviao": {
        "velocidade": "baixa",
        "hp": "alto",
        "pula_linha": False,
    },
    "raposa": {
        "velocidade": "media",
        "hp": "medio",
        "pula_linha": True,
    },
}


# --- Valores numéricos de balanceamento (Fase 2: só movimento, sem dano ainda) ---
NUM_LANES = 3

ENEMY_SPEED = {          # pixels por segundo, andando em direção ao galinheiro
    "gato": 190,
    "gaviao": 60,
    "raposa": 120,
}

ENEMY_HP = {             # ainda não é consumido nesta fase (sem combate)
    "gato": 20,
    "gaviao": 50,
    "raposa": 30,
}

ENEMY_LANE_SWITCH_MIN_INTERVAL = 2.0   # segundos entre tentativas de pulo (raposa)
ENEMY_LANE_SWITCH_MAX_INTERVAL = 4.0
ENEMY_LANE_SWITCH_SPEED = 200          # pixels/s da transição vertical entre linhas

SPAWN_INTERVAL_MS = 1200               # intervalo entre spawns (fixo por enquanto)

# --- Galinha (atributos-base, todas idênticas por enquanto) ---
# Sem HP: galinha nunca toma dano nesse design, então não precisa de vida.
CHICKEN_DANO = 10
CHICKEN_COOLDOWN_MS = 1000             # 1 disparo por segundo (vel. de ataque)
CHICKEN_ALCANCE = 170                  # raio de ataque; alcança as 2 linhas vizinhas
CHICKEN_EGG_SPEED_BASE = 600           # pixels/s do ovo -- agora é atributo DA GALINHA, upgradável

# --- Economia (Fase 4) ---
STARTING_SEEDS = 10000                  # da pra comprar 2 galinhas de largada
CHICKEN_COST = 50
ENEMY_DROP = {"gato": 5, "gaviao": 15, "raposa": 10}
ROUND_CLEAR_BONUS = 20                 # sementes de bonus ao limpar uma onda

# --- Vidas (pintinhos) ---
# Confirmado com o usuario: regenera +1 por rodada (nao reseta pra 3),
# nunca passa do teto.
MAX_PINTINHOS = 20

# --- Ondas / dificuldade (Fase 4) ---
WAVE_BASE_ENEMIES = 2
WAVE_ENEMIES_INCREMENT = 2             # inimigos a mais por rodada
WAVE_SPAWN_INTERVAL_MS = 900
WAVE_STAT_MULTIPLIER_PER_ROUND = 0.08  # +8% HP e velocidade dos inimigos por rodada


def tipos_disponiveis_na_rodada(rodada):
    """Variedade de inimigos cresce com as rodadas (curva de tutorial implicito)."""
    tipos = ["gato"]
    if rodada >= 3:
        tipos.append("gaviao")
    if rodada >= 1:
        tipos.append("raposa")
    return tipos


# --- Upgrades de galinha ---
# 3 atributos upgradáveis: Dano, Vel. de Ataque (frequência) e Vel. do Ovo.
# Sem upgrade de HP -- galinha não toma dano, não precisa de vida.
CHICKEN_MIN_COOLDOWN_MS = 300           # nao deixa a vel. de ataque ficar absurda
UPGRADE_DANO_STEP = 5
UPGRADE_ATQ_STEP_MS = 120               # reduz o cooldown em 120ms por nivel
UPGRADE_OVO_STEP = 80                   # +80 px/s de velocidade do ovo por nivel
UPGRADE_COST_BASE = {"dano": 10, "atq": 15, "ovo": 5}
UPGRADE_COST_INCREMENT = 10             # cada nivel comprado fica mais caro

# --- Itens especiais (Fase 5) ---
# Numeros escolhidos por mim -- o proprio GDD diz que os efeitos exatos
# ficam pra fase de balanceamento, entao ajuste como quiser depois de
ITEM_DROP_CHANCE = 0.15                 # 15% de chance de dropar item ao matar
ITEM_TYPES = ["podre", "gigante", "chupim", "codorna"]
ITEM_LABELS = {
    "podre": "Ovo Podre",
    "gigante": "Ovo Gigante",
    "chupim": "Ovo de Chupim",
    "codorna": "Ovo de Codorna",
}

# Ovo Podre: area de efeito com lentidao + dano de entrada
PODRE_RAIO = 70
PODRE_DURACAO_MS = 3000
PODRE_SLOW_MULT = 0.5                   # metade da velocidade enquanto estiver na poca
PODRE_DANO_ENTRADA = 8                  # dano unico ao entrar na poca (por inimigo)

# Ovo Gigante: dano maior no alvo + respingo nos vizinhos
GIGANTE_DANO_MULT = 3.0
GIGANTE_SPLASH_RAIO = 60
GIGANTE_SPLASH_DANO = 10

# Ovo de Chupim: alvo fica confuso e anda pra tras
CHUPIM_DURACAO_MS = 3000

# Ovo de Codorna: disparo multiplo, dano menor por ovo
CODORNA_QTD_OVOS = 3
CODORNA_DANO_MULT = 0.4
CODORNA_VEL_MULT = 1.3


def lane_y_center(lane_index):
    """Retorna o centro vertical (em pixels) da linha de ataque lane_index (0, 1 ou 2)."""
    band_index = LANE_BAND_INDEXES[lane_index]
    return PLAYFIELD_Y + band_index * BAND_HEIGHT + BAND_HEIGHT / 2


def placement_slot_position(row_index, slot_index):
    """Retorna o (x, y) do CENTRO do espaço de posicionamento
    row_index (0 ou 1), slot_index (0 a 4)."""
    band_index = PLACEMENT_BAND_INDEXES[row_index]
    band_top = PLAYFIELD_Y + band_index * BAND_HEIGHT
    center_y = band_top + BAND_HEIGHT / 2

    if row_index == 0:
        center_y += 0
    elif row_index == 1:
        center_y -= 25    

    slot_width = PLAYFIELD_WIDTH / SLOTS_PER_ROW * 0.73
    center_x = PLAYFIELD_X + slot_width * slot_index + slot_width / 2 + 165
    return center_x, center_y
