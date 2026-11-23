#!/usr/bin/env python3
"""Mede, quadro a quadro, onde existe tinta num vídeo ou numa sequência com alfa.

Regra da peça: todo o tipo no terço de cima, a 6% ou mais de cada borda,
inclusive durante as entradas animadas.

Uso:
  python3 scripts/medir-area-segura.py arquivo.mov
  python3 scripts/medir-area-segura.py pasta-com-png/
"""
import glob
import os
import subprocess
import sys
import tempfile

import numpy as np
from PIL import Image

L, A = 1080, 1920
MARGEM = 0.06
ESQ, DIR, TOPO, BASE = L * MARGEM, L * (1 - MARGEM), A * MARGEM, A / 3
LIMIAR = 3  # alfa acima disso conta como tinta (de 0 a 255)


def quadros(origem):
    if os.path.isdir(origem):
        return sorted(glob.glob(os.path.join(origem, "*.png")))
    pasta = tempfile.mkdtemp(prefix="medir-")
    subprocess.run(
        ["ffmpeg", "-v", "error", "-i", origem, "-pix_fmt", "rgba",
         os.path.join(pasta, "q-%04d.png")],
        check=True,
    )
    return sorted(glob.glob(os.path.join(pasta, "*.png")))


def main():
    origem = sys.argv[1]
    detalhe = "--quadros" in sys.argv
    arquivos = quadros(origem)
    pior = {"esq": L, "dir": 0, "topo": A, "base": 0}
    onde = {}
    vazios = 0
    for n, caminho in enumerate(arquivos):
        alfa = np.asarray(Image.open(caminho).convert("RGBA"))[:, :, 3]
        ys, xs = np.nonzero(alfa > LIMIAR)
        if len(xs) == 0:
            vazios += 1
            continue
        # borda de fora do último pixel com tinta
        caixa = {"esq": xs.min(), "dir": xs.max() + 1, "topo": ys.min(), "base": ys.max() + 1}
        if detalhe:
            print(f"q{n:03d} {n/30:5.2f}s  x {caixa['esq']:4d}..{caixa['dir']:4d}  y {caixa['topo']:4d}..{caixa['base']:4d}")
        for lado, menor in (("esq", True), ("topo", True), ("dir", False), ("base", False)):
            if (caixa[lado] < pior[lado]) if menor else (caixa[lado] > pior[lado]):
                pior[lado] = caixa[lado]
                onde[lado] = n

    print(f"{origem}: {len(arquivos)} quadros, {vazios} sem tinta")
    folgas = {
        "esquerda": (pior["esq"] / L * 100, pior["esq"] >= ESQ, onde.get("esq")),
        "direita": ((L - pior["dir"]) / L * 100, pior["dir"] <= DIR, onde.get("dir")),
        "topo": (pior["topo"] / A * 100, pior["topo"] >= TOPO, onde.get("topo")),
    }
    ok = True
    for lado, (pct, passou, q) in folgas.items():
        ok = ok and passou
        print(f"  margem {lado:8s} mínima: {pct:5.2f}%  (quadro {q})  {'ok' if passou else 'FORA'}")
    passou = pior["base"] <= BASE
    ok = ok and passou
    print(f"  tinta mais baixa: y = {pior['base']} de {A} ({pior['base'] / A * 100:.2f}% da altura; terço = {BASE:.0f})  (quadro {onde.get('base')})  {'ok' if passou else 'FORA'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
