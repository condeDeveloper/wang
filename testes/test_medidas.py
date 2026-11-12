"""Os numeros do README, presos. Varredura completa com teto 3: ~12 s."""

from wang.medidas import (
    QUANTOS_CONJUNTOS,
    distribuicao,
    exemplos,
    fracao_sobrevivente,
    morrem_antes,
    tamanhos_que_ninguem_realiza,
)

DIST_TETO_3 = {0: 1, 1: 248, 2: 72, 3: 65215}


def test_quantos_conjuntos_existem():
    assert QUANTOS_CONJUNTOS == 65536


def test_a_varredura_cobre_tudo():
    dist = distribuicao(3)
    assert sum(dist.values()) == 65536


def test_distribuicao_com_teto_3():
    assert distribuicao(3) == DIST_TETO_3


def test_quase_todo_conjunto_passa_do_3x3():
    assert morrem_antes(3) == 320
    assert distribuicao(3)[3] == 65215
    f = fracao_sobrevivente(3)
    assert 0.995 < f < 0.9952


def test_so_um_conjunto_fica_no_zero():
    """O vazio, e so ele: qualquer ladrilho faz pelo menos 1x1."""
    assert distribuicao(3)[0] == 1


def test_com_teto_3_os_dois_tamanhos_sao_realizados():
    """Com teto 3 a pergunta ainda nao aparece: 1 e 2 tem conjunto.
    O buraco em 3 e 4 so se ve com teto 5, no test_pesados."""
    assert tamanhos_que_ninguem_realiza(3) == ()


def test_menor_exemplo_de_cada_tamanho():
    ex = exemplos(3)
    assert ex[1] == ((0, 0, 0, 1),)
    assert ex[3] == ((0, 0, 0, 0),)
    assert len(ex[2]) == 3


def test_um_ladrilho_liso_ladrilha_tudo():
    """(0,0,0,0) encaixa consigo mesmo nos quatro lados."""
    assert exemplos(3)[3] == ((0, 0, 0, 0),)
