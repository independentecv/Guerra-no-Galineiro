
import random
import pygame
from PPlay.sprite import Sprite
from animacoes import calcular_deslocamento
import config

ENEMY_IMAGES = {
    "gato": "assets/animacoes/gato/gato.png",
    "gaviao": "assets/animacoes/gaviao/gaviao.png",
    "raposa": "assets/animacoes/raposa/raposa.png",
    "cobra": "assets/animacoes/cobra/cobra.png",
}

ENEMY_LABEL = {
    "gato": "Gato",
    "gaviao": "Gaviao",
    "raposa": "Raposa",
    "cobra": "Cobra"
}


class Enemy:

    def __init__(self, tipo, lane_index, multiplicador=1.0):
        self.tipo = tipo

        self.frames_animacao = None
        self.indice_frame = 0
        self.proximo_frame = pygame.time.get_ticks() + 120

        if tipo == "raposa":
            self.frames_animacao = self._carregar_frames_raposa()
            self.sprite = self.frames_animacao[0]

        elif tipo == "gato":
            self.frames_animacao = self._carregar_frames_animacao(6, "gato",0.35)
            self.sprite = self.frames_animacao[0]

        elif tipo == "gaviao":
            self.frames_animacao = self._carregar_frames_animacao(7, "gaviao", 0.80)
            self.sprite = self.frames_animacao[0]
        elif tipo == "cobra":
            self.frames_animacao = self._carregar_frames_animacao(
                8, "cobra", 1.0
            )
            self.sprite = self.frames_animacao[0]
        else:
            self.sprite = Sprite(ENEMY_IMAGES[tipo])

        self.inicio_animacao = pygame.time.get_ticks()
        self.deslocamento_animacao = 0

        self.speed_x = config.ENEMY_SPEED[tipo] * multiplicador
        self.hp_max = int(round(config.ENEMY_HP[tipo] * multiplicador))
        self.hp = self.hp_max
        self.pula_linha = config.ENEMY_STATS[tipo]["pula_linha"]

        self.lane_atual = lane_index
        self.lane_alvo = lane_index
        self.vivo = True
        self.confuso_ate = 0

        x_inicial = 10
        y_inicial = config.lane_y_center(lane_index) - self.sprite.height / 2
        self.sprite.set_position(x_inicial, y_inicial)

        self._proximo_pulo = self._sortear_proximo_pulo()

    def _carregar_frames_raposa(self):
        spritesheet = pygame.image.load(
            ENEMY_IMAGES["raposa"]
        ).convert_alpha()

        largura_frame = spritesheet.get_width() // 6
        altura_frame = spritesheet.get_height()

        frames = []

        for i in range(6):
            quadro = spritesheet.subsurface(
                (i * largura_frame, 0, largura_frame, altura_frame)
            ).copy()

            quadro = pygame.transform.smoothscale(
                quadro,
                (int(largura_frame * 0.5), int(altura_frame * 0.5))
            )

            caminho = f"assets/animacoes/raposa/raposa_frame_{i}.png"
            pygame.image.save(quadro, caminho)
            frames.append(Sprite(caminho))

        return frames
    def _carregar_frames_animacao(self, quantidade, nome, escala=0.5):
        spritesheet = pygame.image.load(
            ENEMY_IMAGES[nome]
        ).convert_alpha()

        largura_frame = spritesheet.get_width() // quantidade
        altura_frame = spritesheet.get_height()

        frames = []

        for i in range(quantidade):
            quadro = spritesheet.subsurface(
                (
                    i * largura_frame,
                    0,
                    largura_frame,
                    altura_frame
                )
            ).copy()

            quadro = pygame.transform.smoothscale(
                quadro,
                (
                    int(largura_frame * escala),
                    int(altura_frame * escala)
                )
            )

            caminho = f"assets/animacoes/{nome}/{nome}_frame_{i}.png"
            pygame.image.save(quadro, caminho)

            frames.append(Sprite(caminho))

        return frames
    def _sortear_proximo_pulo(self):
        return pygame.time.get_ticks() + random.randint(
            int(config.ENEMY_LANE_SWITCH_MIN_INTERVAL * 1000),
            int(config.ENEMY_LANE_SWITCH_MAX_INTERVAL * 1000),
        )

    def _tentar_trocar_linha(self):
        opcoes = [i for i in range(config.NUM_LANES) if i != self.lane_atual]
        self.lane_alvo = random.choice(opcoes)

    def update(self, multiplicador_velocidade=1.0):
        agora = pygame.time.get_ticks()
        self.sprite.y -= self.deslocamento_animacao
        self.deslocamento_animacao = 0

        # Só a raposa decide trocar de linha, e só quando não está no meio de uma troca
        if self.pula_linha and self.lane_atual == self.lane_alvo:
            if agora >= self._proximo_pulo:
                self._tentar_trocar_linha()
                self._proximo_pulo = self._sortear_proximo_pulo()

        # Avanço horizontal (ou recuo, se confuso pelo Ovo de Chupim), com
        # o multiplicador de lentidão da poça do Ovo Podre (se houver)
        velocidade_efetiva = self.speed_x * multiplicador_velocidade
        if agora < self.confuso_ate:
            self.sprite.move_x(-velocidade_efetiva)
        else:
            self.sprite.move_x(velocidade_efetiva)

        # Transição vertical suave quando está migrando de linha
        if self.lane_atual != self.lane_alvo:
            y_alvo = config.lane_y_center(self.lane_alvo) - self.sprite.height / 2
            if self.sprite.y < y_alvo - 4:
                self.sprite.move_y(config.ENEMY_LANE_SWITCH_SPEED)
            elif self.sprite.y > y_alvo + 4:
                self.sprite.move_y(-config.ENEMY_LANE_SWITCH_SPEED)
            else:
                self.sprite.y = y_alvo
                self.lane_atual = self.lane_alvo
        tempo = (agora - self.inicio_animacao) / 1000

        self.deslocamento_animacao = calcular_deslocamento(
            self.tipo, tempo
        )

        self.sprite.y += self.deslocamento_animacao
        if self.frames_animacao is not None and agora >= self.proximo_frame:
            x = self.sprite.x
            y = self.sprite.y

            self.indice_frame = (self.indice_frame + 1) % len(self.frames_animacao)
            self.sprite = self.frames_animacao[self.indice_frame]
            self.sprite.set_position(x, y)

            self.proximo_frame = agora + 120
            
    def chegou_no_galinheiro(self):
        return self.sprite.x + self.sprite.width >= config.GALINHEIRO_X

    def draw(self, janela):
        self.sprite.draw()
        # Rótulo de depuração (linha atual + hp) -- remover quando a arte final
        # e a barra de vida estiverem prontas.
        rotulo = f"{ENEMY_LABEL[self.tipo]} L{self.lane_atual + 1} {self.hp}hp"
        if pygame.time.get_ticks() < self.confuso_ate:
            rotulo += " (confuso)"
        janela.draw_text(rotulo, self.sprite.x - 10, self.sprite.y - 16, cor="black")


class Chicken:

    def __init__(self, centro_x, centro_y):
        self.sprite = Sprite('assets/galinha3.png')
        self.sprite.set_scale(0.9)
        self.frames_ataque = self._carregar_frames_ataque()
        self.indice_frame = 0
        self.atacando = False
        self.tempo_frame = 100
        self.proximo_frame = 0
        self.disparo_realizado = False
        self.sprite.set_position(centro_x - self.sprite.width / 2, centro_y - self.sprite.height / 2)

        self.centro_x = centro_x
        self.centro_y = centro_y

        # Niveis de upgrade -- todas comecam identicas, no nivel 0.
        # Sem HP: a galinha nunca toma dano nesse design.
        self.nivel_dano = 0
        self.nivel_atq = 0
        self.nivel_ovo = 0
        self.alcance = config.CHICKEN_ALCANCE
        self._recalcular_atributos()

        self.selecionada = False
        self._proximo_tiro = 0
        self.item_equipado = None  # None ou um dos config.ITEM_TYPES / afeta só o próximo disparo

        # sprites decorativos (alcance e contorno de selecao)
        self.sprite_alcance = Sprite('assets/alcance.png')
        self.sprite_alcance.set_position(
            centro_x - self.sprite_alcance.width / 2,
            centro_y - self.sprite_alcance.height / 2,
        )
        self.sprite_selecao = Sprite('assets/selecao.png')
        self.sprite_selecao.set_position(
            centro_x - self.sprite_selecao.width / 2,
            centro_y - self.sprite_selecao.height / 2,
        )
    def _carregar_frames_ataque(self):
        caminho = "assets/animacoes/galinha/galinha_attack.png"

        spritesheet = pygame.image.load(caminho).convert_alpha()

        quantidade = 8
        largura_frame = spritesheet.get_width() // quantidade
        altura_frame = spritesheet.get_height()

        frames = []

        for i in range(quantidade):
            quadro = spritesheet.subsurface(
                (i * largura_frame, 0, largura_frame, altura_frame)
            ).copy()

            quadro = pygame.transform.smoothscale(
                quadro,
                (
                    int(largura_frame * 0.9),
                    int(altura_frame * 0.9)
                )
            )

            caminho_frame = f"assets/animacoes/galinha/galinha_attack_frame_{i}.png"
            pygame.image.save(quadro, caminho_frame)

            frames.append(Sprite(caminho_frame))

        return frames
    
    def _recalcular_atributos(self):
        self.dano = config.CHICKEN_DANO + self.nivel_dano * config.UPGRADE_DANO_STEP
        self.cooldown_ms = max(
            config.CHICKEN_MIN_COOLDOWN_MS,
            config.CHICKEN_COOLDOWN_MS - self.nivel_atq * config.UPGRADE_ATQ_STEP_MS,
        )
        self.vel_ovo = config.CHICKEN_EGG_SPEED_BASE + self.nivel_ovo * config.UPGRADE_OVO_STEP

    def nivel_do(self, stat):
        return {"dano": self.nivel_dano, "atq": self.nivel_atq, "ovo": self.nivel_ovo}[stat]

    def custo_upgrade(self, stat):
        return config.UPGRADE_COST_BASE[stat] + self.nivel_do(stat) * config.UPGRADE_COST_INCREMENT

    def aplicar_upgrade(self, stat):
        if stat == "dano":
            self.nivel_dano += 1
        elif stat == "atq":
            self.nivel_atq += 1
        elif stat == "ovo":
            self.nivel_ovo += 1
        self._recalcular_atributos()

    def contem_ponto(self, x, y):
        return (
            self.sprite.x <= x <= self.sprite.x + self.sprite.width and
            self.sprite.y <= y <= self.sprite.y + self.sprite.height
        )

    def _encontrar_alvo(self, inimigos):
        mais_proximo = None
        menor_dist = None
        for inimigo in inimigos:
            ex = inimigo.sprite.x + inimigo.sprite.width / 2
            ey = inimigo.sprite.y + inimigo.sprite.height / 2
            dist = ((ex - self.centro_x) ** 2 + (ey - self.centro_y) ** 2) ** 0.5
            if dist <= self.alcance and (menor_dist is None or dist < menor_dist):
                menor_dist = dist
                mais_proximo = inimigo
        return mais_proximo

    def _encontrar_varios_alvos(self, inimigos, qtd):
        """Usado pelo Ovo de Codorna: pega até `qtd` inimigos distintos mais
        próximos dentro do alcance. Se houver menos inimigos que `qtd`, repete
        o mais próximo pra preencher a rajada."""
        candidatos = []
        for inimigo in inimigos:
            ex = inimigo.sprite.x + inimigo.sprite.width / 2
            ey = inimigo.sprite.y + inimigo.sprite.height / 2
            dist = ((ex - self.centro_x) ** 2 + (ey - self.centro_y) ** 2) ** 0.5
            if dist <= self.alcance:
                candidatos.append((dist, inimigo))
        if not candidatos:
            return []
        candidatos.sort(key=lambda c: c[0])
        alvos = [c[1] for c in candidatos[:qtd]]
        while len(alvos) < qtd:
            alvos.append(candidatos[0][1])
        return alvos

    _SPRITE_POR_ITEM = {
        None: 'assets/ovo.png',
        "podre": 'assets/ovo_podre.png',
        "gigante": 'assets/ovo_gigante.png',
        "chupim": 'assets/ovo_chupim.png',
    }
    def _realizar_disparo(self, inimigos, ovos):
        item = self.item_equipado

        if item == "codorna":
            alvos = self._encontrar_varios_alvos(
                inimigos,
                config.CODORNA_QTD_OVOS
            )

            if not alvos:
                return False

            for alvo in alvos:
                ovos.append(Egg(
                    self.centro_x,
                    self.centro_y,
                    alvo,
                    self.dano * config.CODORNA_DANO_MULT,
                    self.vel_ovo * config.CODORNA_VEL_MULT,
                    tipo_especial="codorna",
                    sprite_path='assets/ovo_codorna.png',
                ))

        else:
            alvo = self._encontrar_alvo(inimigos)

            if alvo is None:
                return False

            dano_final = (
                self.dano * config.GIGANTE_DANO_MULT
                if item == "gigante" else self.dano
            )

            ovos.append(Egg(
                self.centro_x,
                self.centro_y,
                alvo,
                dano_final,
                self.vel_ovo,
                tipo_especial=item,
                sprite_path=self._SPRITE_POR_ITEM[item],
            ))

        self.item_equipado = None
        self._proximo_tiro = pygame.time.get_ticks() + self.cooldown_ms

        return True
    def update(self, inimigos, ovos):
        agora = pygame.time.get_ticks()

        if self.atacando:
            if agora >= self.proximo_frame:
                self.indice_frame += 1

                if self.indice_frame == 2 and not self.disparo_realizado:
                    self._realizar_disparo(inimigos, ovos)
                    self.disparo_realizado = True

                if self.indice_frame >= len(self.frames_ataque):
                    self.atacando = False
                    self.sprite = Sprite('assets/galinha3.png')
                    self.sprite.set_scale(0.9)
                    self.sprite.set_position(
                        self.centro_x - self.sprite.width / 2,
                        self.centro_y - self.sprite.height / 2
                    )
                    return

                self.sprite = self.frames_ataque[self.indice_frame]
                self.sprite.set_position(
                    self.centro_x - self.sprite.width / 2,
                    self.centro_y - self.sprite.height / 2
                )

                self.proximo_frame = agora + self.tempo_frame

            return

        if agora < self._proximo_tiro:
            return

        alvo = self._encontrar_alvo(inimigos)

        if alvo is None:
            return

        self.atacando = True
        self.indice_frame = 0
        self.disparo_realizado = False
        self.sprite = self.frames_ataque[0]
        self.sprite.set_position(
            self.centro_x - self.sprite.width / 2,
            self.centro_y - self.sprite.height / 2
        )
        self.proximo_frame = agora + self.tempo_frame
    def draw_alcance(self):
        self.sprite_alcance.draw()

    def draw(self):
        if self.selecionada:
            self.sprite_selecao.draw()
        self.sprite.draw()
def redimensionar_ovo(caminho, tamanho):
    imagem = pygame.image.load(caminho).convert_alpha()

    area = imagem.get_bounding_rect()
    imagem = imagem.subsurface(area).copy()

    largura, altura = imagem.get_size()
    escala = tamanho / max(largura, altura)

    nova_largura = int(largura * escala)
    nova_altura = int(altura * escala)

    imagem = pygame.transform.smoothscale(
        imagem, (nova_largura, nova_altura)
    )

    caminho_temp = caminho.replace(".png", "_redimensionado.png")
    pygame.image.save(imagem, caminho_temp)

    return Sprite(caminho_temp)

class Egg:

    def __init__(self, x_origem, y_origem, alvo, dano, velocidade, tipo_especial=None, sprite_path='assets/ovo.png'):
        if tipo_especial is None:
            self.sprite = Sprite(sprite_path)

        elif tipo_especial == "gigante":
            self.sprite = redimensionar_ovo(sprite_path, 60)

        elif tipo_especial == "codorna":
            self.sprite = redimensionar_ovo(sprite_path, 40)

        elif tipo_especial == "podre":
            self.sprite = redimensionar_ovo(sprite_path, 20)

        elif tipo_especial == "chupim":
            self.sprite = redimensionar_ovo(sprite_path, 25)

        self.sprite.set_position(
            x_origem - self.sprite.width / 2,
            y_origem - self.sprite.height / 2
        )

        self.dano = dano
        self.alvo = alvo
        self.velocidade = velocidade
        self.tipo_especial = tipo_especial

        self.vx, self.vy = self._direcao_para_alvo(x_origem, y_origem)
    def _direcao_para_alvo(self, origem_x, origem_y):
        alvo_x = self.alvo.sprite.x + self.alvo.sprite.width / 2
        alvo_y = self.alvo.sprite.y + self.alvo.sprite.height / 2
        dx = alvo_x - origem_x
        dy = alvo_y - origem_y
        distancia = max((dx ** 2 + dy ** 2) ** 0.5, 1)
        return (dx / distancia) * self.velocidade, (dy / distancia) * self.velocidade

    def update(self):
        # Enquanto o alvo original estiver vivo, recalcula o rumo (perseguição).
        # Se ele já morreu/chegou no galinheiro, mantém o último rumo reto.
        if self.alvo is not None and self.alvo.vivo:
            centro_x = self.sprite.x + self.sprite.width / 2
            centro_y = self.sprite.y + self.sprite.height / 2
            self.vx, self.vy = self._direcao_para_alvo(centro_x, centro_y)

        self.sprite.move_x(self.vx)
        self.sprite.move_y(self.vy)

    def centro(self):
        return self.sprite.x + self.sprite.width / 2, self.sprite.y + self.sprite.height / 2

    def fora_da_tela(self):
        return (
            self.sprite.x < -20 or self.sprite.x > config.WINDOW_WIDTH + 20 or
            self.sprite.y < -20 or self.sprite.y > config.WINDOW_HEIGHT + 20
        )

    def draw(self):
        self.sprite.draw()


class Puddle:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.raio = config.PODRE_RAIO
        self.expira_em = pygame.time.get_ticks() + config.PODRE_DURACAO_MS
        self._ja_atingiu = set()

        self.frames = self._carregar_frames()
        self.indice_frame = 0
        self.sprite = self.frames[0]

        self.tempo_frame = 120
        self.proximo_frame = pygame.time.get_ticks() + self.tempo_frame

        self.sprite.set_position(
            x - self.sprite.width / 2,
            y - self.sprite.height / 2 - 10
        )

    def _carregar_frames(self):
        caminho = "assets/effects/poca.png"

        spritesheet = pygame.image.load(caminho).convert_alpha()

        quantidade = 12
        largura_frame = spritesheet.get_width() // quantidade
        altura_frame = spritesheet.get_height()

        frames = []

        for i in range(quantidade):
            quadro = spritesheet.subsurface(
                (
                    i * largura_frame,
                    0,
                    largura_frame,
                    altura_frame
                )
            ).copy()

            quadro = pygame.transform.smoothscale(
                quadro,
                (
                    int(largura_frame * 2.5),
                    int(altura_frame * 2.5)
                )
            )

            caminho_frame = f"assets/effects/poca_frame_{i}.png"
            pygame.image.save(quadro, caminho_frame)

            frames.append(Sprite(caminho_frame))

        return frames

    def update(self):
        agora = pygame.time.get_ticks()

        if agora >= self.proximo_frame:
            x = self.sprite.x
            y = self.sprite.y

            self.indice_frame = (
                self.indice_frame + 1
            ) % len(self.frames)

            self.sprite = self.frames[self.indice_frame]
            self.sprite.set_position(x, y)

            self.proximo_frame = agora + self.tempo_frame

    def expirou(self):
        return pygame.time.get_ticks() >= self.expira_em

    def afeta(self, inimigo):
        ex = inimigo.sprite.x + inimigo.sprite.width / 2
        ey = inimigo.sprite.y + inimigo.sprite.height / 2

        dentro = (
            ((ex - self.x) ** 2 + (ey - self.y) ** 2) ** 0.5
            <= self.raio
        )

        if dentro and id(inimigo) not in self._ja_atingiu:
            inimigo.hp -= config.PODRE_DANO_ENTRADA
            self._ja_atingiu.add(id(inimigo))

        return dentro

    def draw(self):
        self.sprite.draw()