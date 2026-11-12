"""Ladrilhos de Wang: quadrados com uma cor em cada borda.

Um ladrilho e uma quadra (norte, leste, sul, oeste). Os ladrilhos nao giram nem
espelham -- essa e a regra do jogo, e e o que torna o problema interessante.
Dois ladrilhos so podem ficar lado a lado se as cores que se encostam forem
iguais:

    A à esquerda de B   exige   A.leste == B.oeste
    A em cima de B      exige   A.sul   == B.norte

Com `c` cores existem exatamente c^4 ladrilhos possiveis, e 2^(c^4) conjuntos.
Para duas cores isso da 16 ladrilhos e **65.536 conjuntos**, que e um dominio
finito pequeno o bastante para varrer inteiro -- e e isso que este projeto faz.
"""

NORTE, LESTE, SUL, OESTE = 0, 1, 2, 3


def todos_os_ladrilhos(cores):
    """Os c^4 ladrilhos possiveis, em ordem fixa."""
    saida = []
    for n in range(cores):
        for l in range(cores):
            for s in range(cores):
                for o in range(cores):
                    saida.append((n, l, s, o))
    return saida


def conjunto_do_indice(mascara, cores):
    """O conjunto de ladrilhos que a mascara de bits descreve.

    A varredura precisa de um nome curto para cada um dos 2^(c^4) conjuntos, e
    um inteiro serve: o bit i diz se o i-esimo ladrilho esta dentro.
    """
    tudo = todos_os_ladrilhos(cores)
    return [t for i, t in enumerate(tudo) if mascara >> i & 1]


def encaixa_lado_a_lado(esquerdo, direito):
    return esquerdo[LESTE] == direito[OESTE]


def encaixa_em_cima(cima, baixo):
    return cima[SUL] == baixo[NORTE]


def grade_valida(grade):
    """A grade ja montada respeita as duas regras?

    `grade[y][x]` e o ladrilho da linha y, coluna x. Serve para conferir o que
    a busca devolve: achar que ladrilhou nao e ter ladrilhado.
    """
    altura = len(grade)
    if altura == 0:
        return True
    largura = len(grade[0])
    for y in range(altura):
        if len(grade[y]) != largura:
            return False
        for x in range(largura):
            if x + 1 < largura and not encaixa_lado_a_lado(grade[y][x], grade[y][x + 1]):
                return False
            if y + 1 < altura and not encaixa_em_cima(grade[y][x], grade[y + 1][x]):
                return False
    return True


def perfil_oeste(coluna):
    """As cores que a coluna mostra para a esquerda, de cima para baixo."""
    return tuple(t[OESTE] for t in coluna)


def perfil_leste(coluna):
    """As cores que a coluna mostra para a direita, de cima para baixo."""
    return tuple(t[LESTE] for t in coluna)
