# -*- coding: utf-8 -*-
"""
Ranking das melhores rodadas alcancadas, salvo em ranking.json
(na mesma pasta do jogo) para sobreviver entre execucoes.
"""
import json
import os
from datetime import datetime

RANKING_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ranking.json")
RANKING_MAX = 10   # quantas posicoes sao guardadas/exibidas



def carregar():
    """Retorna a lista [{"rodada": int, "data": str}, ...] ordenada da melhor
    para a pior. Se o arquivo nao existir ou estiver corrompido, retorna []."""
    try:
        with open(RANKING_PATH, "r", encoding="utf-8") as f:
            dados = json.load(f)
        lista = [
            {"rodada": int(e["rodada"]), "data": str(e.get("data", ""))}
            for e in dados
            if isinstance(e, dict) and "rodada" in e
        ]
        lista.sort(key=lambda e: -e["rodada"])
        return lista[:RANKING_MAX]
    except (OSError, ValueError, TypeError, KeyError):
        return []


def _salvar(lista):
    try:
        with open(RANKING_PATH, "w", encoding="utf-8") as f:
            json.dump(lista, f, ensure_ascii=False, indent=2)
    except OSError:
        pass  # sem permissao de escrita: o jogo continua normalmente


def registrar(rodada):
    """Adiciona uma partida ao ranking. Retorna a posicao (1 = melhor) em que
    ela entrou, ou None se nao ficou entre as RANKING_MAX melhores."""
    lista = carregar()
    nova = {"rodada": int(rodada), "data": datetime.now().strftime("%d/%m/%Y")}
    # em empate, a partida mais antiga fica na frente (insere depois dos iguais)
    pos = 0
    while pos < len(lista) and lista[pos]["rodada"] >= nova["rodada"]:
        pos += 1
    lista.insert(pos, nova)
    lista = lista[:RANKING_MAX]
    _salvar(lista)
    return pos + 1 if pos < RANKING_MAX else None
