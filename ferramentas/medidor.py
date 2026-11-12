"""Medidor: as tabelas do README em markdown.

    python ferramentas/medidor.py           teto 3 (12 s)
    python ferramentas/medidor.py --fundo   teto 5 (346 s)
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wang.medidas import (  # noqa: E402
    QUANTOS_CONJUNTOS,
    amostra_de_sobreviventes,
    distribuicao,
    exemplos,
    fracao_sobrevivente,
    morrem_antes,
    quantos_morrem_depois,
    tamanhos_que_ninguem_realiza,
)


def main():
    teto = 5 if '--fundo' in sys.argv else 3
    t0 = time.time()

    print('## Varredura completa dos %d conjuntos (teto %d)' % (QUANTOS_CONJUNTOS, teto))
    print()
    dist = distribuicao(teto)
    print('| maior quadrado | conjuntos |')
    print('|---|---|')
    for n in sorted(dist):
        print('| %d%s | %d |' % (n, ' (teto)' if n == teto else '', dist[n]))

    print()
    print('tamanhos que ninguem realiza: %s'
          % (', '.join(str(v) for v in tamanhos_que_ninguem_realiza(teto)) or 'nenhum'))
    print('morrem antes do teto: %d' % morrem_antes(teto))
    print('chegam ao teto: %d (%.2f%%)' % (dist.get(teto, 0), 100 * fracao_sobrevivente(teto)))

    print()
    print('## Menor conjunto por tamanho')
    print()
    for n, conj in sorted(exemplos(teto).items()):
        print('- n=%d: %d ladrilho(s), %s' % (n, len(conj), list(conj)))

    if '--fundo' in sys.argv:
        print()
        print('## Sondagem dos sobreviventes em 6, 7 e 8')
        print()
        amostra = amostra_de_sobreviventes(teto, 300)
        mortos = quantos_morrem_depois(amostra, (6, 7, 8))
        print('de %d sobreviventes, morreram depois: %d' % (len(amostra), mortos))

    print()
    print('medido em %.1f s' % (time.time() - t0))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
