"""Linha de comando.

    python -m wang             a varredura completa com teto 3
    python -m wang fundo       a varredura lenta, com teto 5
"""

import sys
import time

from .medidas import (
    QUANTOS_CONJUNTOS,
    distribuicao,
    exemplos,
    fracao_sobrevivente,
    morrem_antes,
    tamanhos_que_ninguem_realiza,
)


def mostra(teto):
    t0 = time.time()
    dist = distribuicao(teto)
    print('varredura completa dos %d conjuntos de duas cores (teto %d)'
          % (QUANTOS_CONJUNTOS, teto))
    print()
    print('maior quadrado ladrilhavel -> quantos conjuntos')
    for n in sorted(dist):
        rotulo = '%d (teto)' % n if n == teto else str(n)
        print('   %-10s %d' % (rotulo, dist[n]))
    print()
    vazios = tamanhos_que_ninguem_realiza(teto)
    if vazios:
        print('NENHUM conjunto morre em: %s' % ', '.join(str(v) for v in vazios))
    else:
        print('todo tamanho ate %d e realizado por algum conjunto' % (teto - 1))
    print('morrem antes do teto: %d' % morrem_antes(teto))
    print('chegam ao teto: %d (%.2f%%)' % (dist.get(teto, 0), 100 * fracao_sobrevivente(teto)))
    print()
    print('menor conjunto que alcanca cada tamanho:')
    for n, conj in sorted(exemplos(teto).items()):
        print('   n=%d  %d ladrilho(s)  %s' % (n, len(conj), list(conj)))
    print()
    print('medido em %.1f s' % (time.time() - t0))


def main():
    teto = 5 if len(sys.argv) > 1 and sys.argv[1] == 'fundo' else 3
    mostra(teto)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
