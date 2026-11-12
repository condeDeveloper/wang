"""Ladrilhos, encaixe e grades."""

from wang.nucleo import (
    conjunto_do_indice,
    encaixa_em_cima,
    encaixa_lado_a_lado,
    grade_valida,
    perfil_leste,
    perfil_oeste,
    todos_os_ladrilhos,
)


def test_quantos_ladrilhos_existem():
    assert len(todos_os_ladrilhos(2)) == 16
    assert len(todos_os_ladrilhos(3)) == 81
    assert len(set(todos_os_ladrilhos(2))) == 16


def test_conjunto_do_indice_le_os_bits():
    assert conjunto_do_indice(0, 2) == []
    assert conjunto_do_indice(1, 2) == [(0, 0, 0, 0)]
    assert len(conjunto_do_indice((1 << 16) - 1, 2)) == 16


def test_encaixe_olha_as_bordas_certas():
    """O encaixe tem lado: A-depois-de-B nao e B-depois-de-A.

    O par precisa ser mesmo assimetrico. Com a=(0,1,0,0) e b=(0,0,0,1) a volta
    TAMBEM casa, porque o leste de b e o oeste de a valem os dois zero -- isso
    testaria nada.
    """
    a = (0, 1, 0, 0)   # leste = 1, oeste = 0
    b = (0, 1, 0, 1)   # leste = 1, oeste = 1
    assert encaixa_lado_a_lado(a, b)        # 1 contra 1
    assert not encaixa_lado_a_lado(b, a)    # 1 contra 0

    c = (0, 0, 1, 0)   # sul = 1, norte = 0
    d = (1, 0, 1, 0)   # norte = 1, sul = 1
    assert encaixa_em_cima(c, d)            # 1 contra 1
    assert not encaixa_em_cima(d, c)        # 1 contra 0


def test_ladrilho_nao_gira():
    """Girar e proibido: (0,1,0,0) nao vira (0,0,0,1)."""
    a = (0, 1, 0, 0)
    assert not encaixa_lado_a_lado(a, a)


def test_grade_valida_reprova_de_verdade():
    liso = (0, 0, 0, 0)
    assert grade_valida([[liso, liso], [liso, liso]])
    assert grade_valida([])
    torto = (0, 1, 0, 0)
    assert not grade_valida([[torto, torto]])


def test_perfis():
    coluna = [(0, 1, 0, 0), (0, 0, 0, 1)]
    assert perfil_oeste(coluna) == (0, 1)
    assert perfil_leste(coluna) == (1, 0)
