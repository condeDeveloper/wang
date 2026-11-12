"""As tabelas do README.

Duas varreduras completas dos mesmos 65.536 conjuntos, com tetos diferentes:

- **teto 3** leva 12 segundos e e a que a bateria roda;
- **teto 5** leva 346 segundos e foi rodada uma vez, para estabelecer que
  NENHUM conjunto morre em 3 nem em 4.

O segundo fato e o que justifica o primeiro: se nada morre entre 3 e 5, a
particao obtida com teto 3 e a mesma que a de teto 5, e a bateria pode usar a
barata sem perder informacao. Isso esta escrito aqui porque e um argumento, e
argumento nao conferido e chute: o `test_pesados.py` refaz a varredura de teto
5 e cobra a igualdade.
"""

from functools import lru_cache

from .busca import alcancavel, maior_quadrado
from .nucleo import conjunto_do_indice

CORES = 2
QUANTOS_CONJUNTOS = 1 << (CORES ** 4)


@lru_cache(maxsize=None)
def varredura(teto):
    """Para cada um dos 65.536 conjuntos, o maior quadrado que ele ladrilha.

    Devolve (distribuicao, menor_exemplo_por_tamanho).
    """
    dist = {}
    primeiro = {}
    for mascara in range(QUANTOS_CONJUNTOS):
        conj = conjunto_do_indice(mascara, CORES)
        if not conj:
            dist[0] = dist.get(0, 0) + 1
            continue
        n = maior_quadrado(conj, teto)
        dist[n] = dist.get(n, 0) + 1
        if n not in primeiro:
            primeiro[n] = tuple(conj)
    return tuple(sorted(dist.items())), tuple(sorted(primeiro.items()))


def distribuicao(teto=3):
    return dict(varredura(teto)[0])


def exemplos(teto=3):
    return dict(varredura(teto)[1])


def tamanhos_que_ninguem_realiza(teto=3):
    """Os tamanhos entre 1 e teto-1 que NENHUM conjunto tem como maximo.

    Um tamanho vazio aqui significa: nao existe conjunto que ladrilhe aquele
    quadrado e falhe no seguinte. E a pergunta inteira deste projeto.
    """
    dist = distribuicao(teto)
    return tuple(n for n in range(1, teto) if dist.get(n, 0) == 0)


def sobreviventes(teto=3):
    return distribuicao(teto).get(teto, 0)


def fracao_sobrevivente(teto=3):
    return sobreviventes(teto) / QUANTOS_CONJUNTOS


def morrem_antes(teto=3):
    """Quantos conjuntos nao chegam ao teto, sem contar o vazio."""
    dist = distribuicao(teto)
    return sum(q for n, q in dist.items() if 1 <= n < teto)


def amostra_de_sobreviventes(teto, quantos, passo=211):
    """Alguns conjuntos que chegaram ao teto, para sondar tamanhos maiores."""
    saida = []
    mascara = 0
    while len(saida) < quantos and mascara < QUANTOS_CONJUNTOS:
        conj = conjunto_do_indice(mascara, CORES)
        if conj and maior_quadrado(conj, teto) == teto:
            saida.append(tuple(conj))
        mascara += passo
    return tuple(saida)


def quantos_morrem_depois(conjuntos, tamanhos):
    """Dos conjuntos dados, quantos falham em algum dos tamanhos."""
    mortos = 0
    for conj in conjuntos:
        for n in tamanhos:
            if not alcancavel(list(conj), n, n):
                mortos += 1
                break
    return mortos
