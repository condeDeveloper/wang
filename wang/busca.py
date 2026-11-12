"""A matriz de transferencia: parar de pensar em celulas e pensar em colunas.

A busca na marra enche a grade celula a celula e refaz trabalho sem parar: a
quinta coluna nao se importa com COMO as quatro primeiras ficaram, so com a
cor que elas mostram para a direita. Esse "so com" e a matriz de transferencia.

Para uma altura fixa, uma coluna inteira se resume a duas coisas: o perfil de
cores que ela mostra para a esquerda e o que ela mostra para a direita. Entao
monta-se a matriz

    A[w][e] = quantas colunas validas tem perfil oeste w e perfil leste e

e o numero de ladrilhamentos de largura m e a SOMA DE TODAS AS ENTRADAS de
A^m: cada caminho w1 -> e1 = w2 -> e2 = w3 ... e um ladrilhamento, e as pontas
ficam livres porque a grade nao tem borda obrigada.

Com c cores e altura h a matriz tem c^h linhas, nao |conjunto|^h. E essa troca
que faz a varredura dos 65.536 conjuntos caber.
"""

from .nucleo import LESTE, NORTE, OESTE, SUL


def colunas_por_perfil(conjunto, altura):
    """A matriz A, como dicionario de dicionarios.

    Monta empilhando ladrilho por ladrilho e carregando tres coisas: o perfil
    oeste ate aqui, o perfil leste ate aqui, e a cor sul do ultimo posto (que
    e a unica coisa que a linha de baixo precisa saber).
    """
    if altura == 0:
        return {(): {(): 1}}
    estados = {((), (), None): 1}
    for _ in range(altura):
        novos = {}
        for (w, e, sul), quantos in estados.items():
            for t in conjunto:
                if sul is not None and t[NORTE] != sul:
                    continue
                chave = (w + (t[OESTE],), e + (t[LESTE],), t[SUL])
                novos[chave] = novos.get(chave, 0) + quantos
        estados = novos
    matriz = {}
    for (w, e, _), quantos in estados.items():
        matriz.setdefault(w, {})
        matriz[w][e] = matriz[w].get(e, 0) + quantos
    return matriz


def _multiplica(a, b):
    saida = {}
    for w, meio in a.items():
        acumulado = {}
        for m, q1 in meio.items():
            for e, q2 in b.get(m, {}).items():
                acumulado[e] = acumulado.get(e, 0) + q1 * q2
        if acumulado:
            saida[w] = acumulado
    return saida


def conta(conjunto, largura, altura):
    """Quantos ladrilhamentos de largura x altura o conjunto permite."""
    if largura == 0 or altura == 0:
        return 1
    if not conjunto:
        return 0
    a = colunas_por_perfil(conjunto, altura)
    potencia = a
    for _ in range(largura - 1):
        potencia = _multiplica(potencia, a)
        if not potencia:
            return 0
    return sum(sum(linha.values()) for linha in potencia.values())


def alcancavel(conjunto, largura, altura):
    """So "da ou nao da", sem contar.

    Para a varredura dos 65.536 conjuntos, contar e desperdicio: os numeros
    ficam enormes e a resposta e um sim ou nao. Aqui so se propaga o conjunto
    de perfis alcancaveis, que nunca passa de c^altura.
    """
    if largura == 0 or altura == 0:
        return True
    if not conjunto:
        return False
    a = colunas_por_perfil(conjunto, altura)
    if not a:
        return False

    # Depois de UMA coluna, os perfis leste possiveis sao todos os que
    # aparecem na matriz: a borda esquerda e livre, entao todo perfil oeste
    # serve de comeco.
    alcancados = set()
    for destinos in a.values():
        alcancados.update(destinos)
    if not alcancados:
        return False

    # Cada coluna seguinte so pode comecar onde a anterior terminou.
    for _ in range(largura - 1):
        seguintes = set()
        for w in alcancados:
            seguintes.update(a.get(w, {}))
        if not seguintes:
            return False
        alcancados = seguintes
    return True


def maior_quadrado(conjunto, teto):
    """O maior N com N x N ladrilhavel, pelo caminho da matriz.

    Vale a monotonicidade: toda grade (N+1) x (N+1) contem uma N x N dentro,
    entao assim que um tamanho falha os maiores falham junto.
    """
    n = 0
    while n < teto and alcancavel(conjunto, n + 1, n + 1):
        n += 1
    return n
