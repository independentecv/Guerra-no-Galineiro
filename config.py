
# --- oiii nilo
WINDOW_WIDTH = 960
WINDOW_TITLE = "Guerra no Galinheiro"

PLAYFIELD_HEIGHT = 600
TOP_UI_HEIGHT = 0
BOTTOM_UI_HEIGHT = 0
PLAYFIELD_Y = 0
WINDOW_HEIGHT = PLAYFIELD_HEIGHT


def set_ui_heights(top, bottom):
    global TOP_UI_HEIGHT, BOTTOM_UI_HEIGHT, PLAYFIELD_Y, WINDOW_HEIGHT
    TOP_UI_HEIGHT = int(top)
    BOTTOM_UI_HEIGHT = int(bottom)
    PLAYFIELD_Y = TOP_UI_HEIGHT
    WINDOW_HEIGHT = TOP_UI_HEIGHT + PLAYFIELD_HEIGHT + BOTTOM_UI_HEIGHT


# --- Zonas laterais ---
FOREST_WIDTH = 140
GALINHEIRO_WIDTH = 140

PLAYFIELD_X = FOREST_WIDTH
PLAYFIELD_WIDTH = WINDOW_WIDTH - FOREST_WIDTH - GALINHEIRO_WIDTH
GALINHEIRO_X = WINDOW_WIDTH - GALINHEIRO_WIDTH


# --- Faixas horizontais do campo ---
NUM_BANDS = 5
BAND_HEIGHT = PLAYFIELD_HEIGHT // NUM_BANDS

LANE_BAND_INDEXES = [0, 2, 4]
PLACEMENT_BAND_INDEXES = [1, 3]


# --- Espaços de posicionamento das galinhas ---
SLOTS_PER_ROW = 5
NEST_WIDTH = 96
NEST_HEIGHT = 64


# --- Atributos dos inimigos ---
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
    "cobra": {
        "velocidade": "alta",
        "hp": "baixo",
        "pula_linha": False,
    }
}


# --- Valores numéricos dos inimigos ---
NUM_LANES = 3

ENEMY_SPEED = {
    "gato": 190,
    "gaviao": 60,
    "raposa": 120,
    "cobra": 150,
}

ENEMY_HP = {
    "gato": 20,
    "gaviao": 50,
    "raposa": 30,
    "cobra": 60,
}

ENEMY_LANE_SWITCH_MIN_INTERVAL = 2.0
ENEMY_LANE_SWITCH_MAX_INTERVAL = 4.0
ENEMY_LANE_SWITCH_SPEED = 200

SPAWN_INTERVAL_MS = 1200


# --- Galinha ---
CHICKEN_DANO = 10
CHICKEN_COOLDOWN_MS = 1000
CHICKEN_ALCANCE = 170
CHICKEN_EGG_SPEED_BASE = 600


# --- Economia ---
STARTING_SEEDS = 10000
CHICKEN_COST = 50

ENEMY_DROP = {
    "gato": 5,
    "gaviao": 15,
    "raposa": 10,
    "cobra": 10,
}

ROUND_CLEAR_BONUS = 20


# --- Vidas ---
MAX_PINTINHOS = 20


# --- Ondas / dificuldade ---
WAVE_BASE_ENEMIES = 2
WAVE_ENEMIES_INCREMENT = 2
WAVE_SPAWN_INTERVAL_MS = 800
WAVE_STAT_MULTIPLIER_PER_ROUND = 0.09


def tipos_disponiveis_na_rodada(rodada):
    tipos = ["gato"]

    if rodada >= 3:
        tipos.append("gaviao")

    if rodada >= 5:
        tipos.append("raposa")

    if rodada >= 2:
        tipos.append("cobra")

    return tipos


# --- Upgrades de galinha ---
CHICKEN_MIN_COOLDOWN_MS = 300
UPGRADE_DANO_STEP = 5
UPGRADE_ATQ_STEP_MS = 120
UPGRADE_OVO_STEP = 80

UPGRADE_COST_BASE = {
    "dano": 10,
    "atq": 15,
    "ovo": 5,
}

UPGRADE_COST_INCREMENT = 10


# --- Itens especiais ---
ITEM_DROP_CHANCE = 0.90

ITEM_TYPES = ["podre", "gigante", "chupim", "codorna"]

ITEM_LABELS = {
    "podre": "Ovo Podre",
    "gigante": "Ovo Gigante",
    "chupim": "Ovo de Chupim",
    "codorna": "Ovo de Codorna",
}


# --- Ovo Podre ---
PODRE_RAIO = 70
PODRE_DURACAO_MS = 3000
PODRE_SLOW_MULT = 0.5
PODRE_DANO_ENTRADA = 8


# --- Ovo Gigante ---
GIGANTE_DANO_MULT = 3.0
GIGANTE_SPLASH_RAIO = 60
GIGANTE_SPLASH_DANO = 10


# --- Ovo de Chupim ---
CHUPIM_DURACAO_MS = 3000


# --- Ovo de Codorna ---
CODORNA_QTD_OVOS = 3
CODORNA_DANO_MULT = 0.4
CODORNA_VEL_MULT = 1.3


def lane_y_center(lane_index):
    band_index = LANE_BAND_INDEXES[lane_index]
    return PLAYFIELD_Y + band_index * BAND_HEIGHT + BAND_HEIGHT / 2


def placement_slot_position(row_index, slot_index):
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
