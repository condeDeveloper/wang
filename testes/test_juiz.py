"""A matriz de transferencia contra a marra.

Os dois metodos nao compartilham uma linha: um empilha colunas e eleva uma
matriz a uma potencia, o outro enche celula por celula e volta atras. Se
concordam em milhares de casos, o rapido esta certo.
"""

from wang.busca import alcancavel, conta
from wang.juiz import conta_ladrilhamentos, ladrilha, maior_quadrado
from wang.nucleo import conjunto_do_indice, grade_valida


def test_o_juiz_recusa_de_verdade():
    """Um ladrilho cujo leste nao casa com o proprio oeste nao faz 2x1."""
    so_um = [(0, 1, 0, 0)]
    assert ladrilha(so_um, 1, 1) is not None
    assert ladrilha(so_um, 2, 1) is None
    assert conta_ladrilhamentos(so_um, 2, 1) == 0


def test_conjunto_vazio_nao_ladrilha_nada():
    assert ladrilha([], 1, 1) is None
    assert conta([], 1, 1) == 0
    assert not alcancavel([], 1, 1)


def test_grade_de_tamanho_zero_e_trivial():
    assert ladrilha([(0, 0, 0, 0)], 0, 3) == []
    assert conta([(0, 0, 0, 0)], 0, 3) == 1


def test_matriz_contra_marra_na_contagem():
    """7.146 comparacoes, conjuntos de ate 4 ladrilhos."""
    comparacoes = 0
    for mascara in range(4096):
        conj = conjunto_do_indice(mascara, 2)
        if len(conj) > 4:
            continue
        for larg in (1, 2, 3):
            for alt in (1, 2, 3):
                comparacoes += 1
                assert conta(conj, larg, alt) == conta_ladrilhamentos(conj, larg, alt), \
                    (conj, larg, alt)
    assert comparacoes == 7146


def test_matriz_contra_marra_no_sim_ou_nao():
    """2.382 comparacoes de ladrilhabilidade."""
    comparacoes = 0
    for mascara in range(4096):
        conj = conjunto_do_indice(mascara, 2)
        if len(conj) > 4:
            continue
        for n in (1, 2, 3):
            comparacoes += 1
            assert alcancavel(conj, n, n) == (ladrilha(conj, n, n) is not None), (conj, n)
    assert comparacoes == 2382


def test_o_que_a_marra_devolve_e_grade_valida():
    for mascara in range(2048):
        conj = conjunto_do_indice(mascara, 2)
        if len(conj) > 4 or not conj:
            continue
        g = ladrilha(conj, 3, 3)
        if g is not None:
            assert grade_valida(g), conj


def test_os_dois_maiores_quadrados_concordam():
    """maior_quadrado existe nos dois arquivos, por caminhos diferentes."""
    from wang.busca import maior_quadrado as pela_matriz
    for mascara in range(0, 2048, 7):
        conj = conjunto_do_indice(mascara, 2)
        if len(conj) > 4 or not conj:
            continue
        assert pela_matriz(conj, 3) == maior_quadrado(conj, 3), conj
