#!/usr/bin/env python3
"""Consulta o historico editorial (references/posts-180d.psv).

Uso (a partir da pasta da skill):
    python3 -I scripts/resumo.py                 # periodo, defasagem e ultimas 30 teses
    python3 -I scripts/resumo.py --n 40          # ultimas 40 publicacoes
    python3 -I scripts/resumo.py --eixo AB       # todas as teses de um eixo (180 dias)
    python3 -I scripts/resumo.py --busca clivagem  # busca por palavra na tese

Este script descreve o arquivo. Nao calcula nota, limiar nem previsao.
"""
import argparse
import datetime as dt
import pathlib
import sys
from collections import Counter

ARQ = pathlib.Path(__file__).resolve().parent.parent / "references" / "posts-180d.psv"
COLS = ["data", "fmt", "codigo", "views", "alcance", "compart", "salvos",
        "curtidas", "coment", "ret_ms", "skip3s", "cta", "eixo", "flags", "tese"]
FMT = {"R": "Reel", "C": "Carrossel", "I": "Imagem"}


def carregar():
    linhas = []
    cabecalho_visto = False
    with ARQ.open(encoding="utf-8") as f:
        for n, bruta in enumerate(f, 1):
            bruta = bruta.rstrip("\n")
            if not bruta or bruta.startswith("#"):
                continue
            campos = bruta.split("|")
            if not cabecalho_visto:
                if campos != COLS:
                    sys.exit(f"linha {n}: cabecalho inesperado")
                cabecalho_visto = True
                continue
            if len(campos) != len(COLS):
                sys.exit(f"linha {n}: {len(campos)} campos, esperado {len(COLS)}")
            r = dict(zip(COLS, campos))
            r["data"] = dt.date.fromisoformat(r["data"])
            linhas.append(r)
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=30)
    ap.add_argument("--eixo")
    ap.add_argument("--busca")
    a = ap.parse_args()

    p = carregar()
    ini, fim = p[-1]["data"], p[0]["data"]
    hoje = dt.date.today()
    print(f"Arquivo: {len(p)} publicacoes, de {ini} a {fim}.")
    atraso = (hoje - fim).days
    print(f"Hoje: {hoje}. Ultima publicacao registrada ha {atraso} dia(s).")
    if atraso > 2:
        print("AVISO: historico possivelmente desatualizado. Atualize pelo Windsor "
              "(references/leitura-dos-dados.md) ou registre a limitacao em uma linha.")
    print("Posts dos ultimos 7 dias do arquivo ainda podem estar acumulando metricas.\n")

    if a.eixo or a.busca:
        sel = p
        if a.eixo:
            sel = [r for r in sel if r["eixo"] == a.eixo.upper()]
        if a.busca:
            b = a.busca.lower()
            sel = [r for r in sel if b in r["tese"].lower()]
        print(f"{len(sel)} publicacao(oes) encontrada(s):")
        for r in sel:
            print(f"  {r['data']} {FMT.get(r['fmt'], r['fmt']):9} {r['eixo']} {r['tese']}")
        return

    ult = p[:a.n]
    print(f"Ultimas {len(ult)} publicacoes (a tese nova nao pode repetir nenhuma delas):")
    for r in ult:
        print(f"  {r['data']} {FMT.get(r['fmt'], r['fmt']):9} {r['eixo']:2} {r['tese']}")

    print("\nEixos nas ultimas publicacoes listadas (contagem descritiva):")
    for e, c in Counter(r["eixo"] for r in ult).most_common():
        print(f"  {e}: {c}")
    print("\nEixos no arquivo inteiro:")
    for e, c in Counter(r["eixo"] for r in p).most_common():
        print(f"  {e}: {c}")


if __name__ == "__main__":
    main()
