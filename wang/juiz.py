"""O juiz: ladrilhar na marra, celula por celula.

Este arquivo nao sabe o que e matriz de transferencia. Ele enche a grade da
esquerda para a direita, de cima para baixo, testando as duas regras a cada
celula e voltando atras quando trava. E lento e obviamente correto, que e o
par de qualidades que se quer num juiz.

A `busca.py` responde a mesma pergunta por um caminho completamente diferente:
agrupa colunas inteiras em estados e eleva uma matriz a uma potencia. Os dois
metodos nao compartilham uma linha. Se discordarem, um dos dois esta errado --
e e isso que se quer descobrir antes de a tabela existir.
"""

from .nucleo import encaixa_em_cima, encaixa_lado_a_lado


def ladrilha(conjunto, largura, altura):
    """Devolve uma grade altura x largura, ou None se nao der.

    Busca com retrocesso pura: nenhuma poda esperta, nenhuma memoria.
    """
    if largura == 0 or altura == 0:
        return []
    if not conjunto:
        return None
    grade = [[None] * largura for _ in range(altura)]

    def desce(pos):
        if pos == largura * altura:
            return True
        y, x = divmod(pos, largura)
        for t in conjunto:
            if x > 0 and not encaixa_lado_a_lado(grade[y][x - 1], t):
                continue
            if y > 0 and not encaixa_em_cima(grade[y - 1][x], t):
                continue
            grade[y][x] = t
            if desce(pos + 1):
                return True
            grade[y][x] = None
        return False

    return grade if desce(0) else None


def conta_ladrilhamentos(conjunto, largura, altura):
    """Quantas grades distintas o conjunto consegue montar.

    Tambem na marra: desce todos os ramos ate o fim. Serve para julgar a
    contagem da matriz de transferencia nos casos pequenos.
    """
    if largura == 0 or altura == 0:
        return 1
    if not conjunto:
        return 0
    grade = [[None] * largura for _ in range(altura)]
    total = [0]

    def desce(pos):
        if pos == largura * altura:
            total[0] += 1
            return
        y, x = divmod(pos, largura)
        for t in conjunto:
            if x > 0 and not encaixa_lado_a_lado(grade[y][x - 1], t):
                continue
            if y > 0 and not encaixa_em_cima(grade[y - 1][x], t):
                continue
            grade[y][x] = t
            desce(pos + 1)
            grade[y][x] = None

    desce(0)
    return total[0]


def maior_quadrado(conjunto, teto):
    """O maior N com N x N ladrilhavel, medido na marra, limitado por `teto`.

    Usa a monotonicidade: se N x N nao da, (N+1) x (N+1) tambem nao da, porque
    todo ladrilhamento maior contem um menor dentro dele.
    """
    n = 0
    while n < teto and ladrilha(conjunto, n + 1, n + 1) is not None:
        n += 1
    return n
