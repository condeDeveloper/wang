"""Os casos lentos, e o argumento que o projeto inteiro depende.

A varredura com teto 5 leva uns 6 minutos. Ela esta aqui porque e a UNICA que
estabelece o achado central: nenhum conjunto de duas cores morre em 3 nem em
4. Sem ela, a frase "teto 3 da a mesma particao que teto 5" seria um
argumento confortavel e nao conferido.
"""

from wang.medidas import (
    amostra_de_sobreviventes,
    distribuicao,
    quantos_morrem_depois,
    tamanhos_que_ninguem_realiza,
)

DIST_TETO_5 = {0: 1, 1: 248, 2: 72, 5: 65215}


def test_distribuicao_com_teto_5():
    assert distribuicao(5) == DIST_TETO_5


def test_ninguem_morre_em_3_nem_em_4():
    """O achado central, medido: os tamanhos 3 e 4 ficam vazios."""
    assert tamanhos_que_ninguem_realiza(5) == (3, 4)


def test_teto_3_e_teto_5_dao_a_mesma_particao():
    """O que justifica a bateria rapida usar o teto 3.

    Quem morre cedo morre igual nos dois; quem chega ao teto e o mesmo monte.
    """
    t3, t5 = distribuicao(3), distribuicao(5)
    assert t3[0] == t5[0] == 1
    assert t3[1] == t5[1] == 248
    assert t3[2] == t5[2] == 72
    assert t3[3] == t5[5] == 65215


def test_sobreviventes_nao_morrem_em_6_7_nem_8():
    """300 sobreviventes sondados mais fundo: nenhum falha."""
    amostra = amostra_de_sobreviventes(5, 300)
    assert len(amostra) == 300
    assert quantos_morrem_depois(amostra, (6, 7, 8)) == 0
