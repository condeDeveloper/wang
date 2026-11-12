# wang

Ladrilhos de Wang varridos **conjunto a conjunto** em Python 3.10+, sem dependência
nenhuma: os 65.536 conjuntos possíveis com duas cores, todos, com a matriz de
transferência fazendo a conta e a busca na marra julgando se ela está certa.

## O que é

Um ladrilho de Wang é um quadrado com uma cor em cada borda. Eles **não giram nem
espelham** — essa é a regra, e é o que torna o problema interessante. Dois ladrilhos só
ficam lado a lado se as cores que se encostam forem iguais.

Com `c` cores existem `c⁴` ladrilhos e `2^(c⁴)` conjuntos. Para duas cores: **16 ladrilhos
e 65.536 conjuntos**, um domínio finito pequeno o bastante para varrer inteiro.

A pergunta: dado um conjunto, qual o maior quadrado `N×N` que ele consegue ladrilhar?

## Os quatro achados

- **Nenhum conjunto de duas cores morre em 3 nem em 4.** Varrendo os 65.536 com teto 5, a
  distribuição tem buraco: 248 conjuntos param no 1×1, 72 param no 2×2, e os outros 65.215
  chegam ao teto. Os tamanhos 3 e 4 ficam **vazios**. Ou o conjunto falha logo, ou passa de
  tudo — não existe conjunto-armadilha com duas cores.
- **99,51% dos conjuntos ladrilham o 5×5.** São 65.215 de 65.536. Só 320 falham antes, e
  **248 deles já morrem no 2×2** — a esmagadora maioria dos fracassos acontece no primeiro
  encaixe que se tenta.
- **300 sobreviventes sondados em 6×6, 7×7 e 8×8: nenhum morreu.** Passar do 3×3 é, na
  prática, passar de tudo que dá para medir aqui.
- **A matriz de transferência acerta nas 9.528 conferências contra a marra**, sem uma
  divergência — 7.146 contagens exatas e 2.382 decisões de sim ou não. E ela troca `|S|^h`
  estados por `c^h`, que é exatamente o que faz a varredura completa caber em minutos.

## A varredura completa

| maior quadrado | conjuntos |
|---|---|
| 0 | 1 |
| 1 | 248 |
| 2 | 72 |
| 3 | **0** |
| 4 | **0** |
| 5 (teto) | 65.215 |

O único conjunto no zero é o vazio: qualquer ladrilho faz pelo menos `1×1`.

| medida | valor |
|---|---|
| conjuntos varridos | 65.536 |
| morrem antes do teto | 320 |
| chegam ao teto | 65.215 (99,51%) |
| tamanhos que ninguém realiza | 3 e 4 |

Menor conjunto de cada tamanho:

- `N=1`: um ladrilho só, `(0,0,0,1)` — o leste é 0 e o oeste é 1, então ele não encosta
  nem nele mesmo.
- `N=2`: três ladrilhos, `(0,0,1,0)`, `(0,1,1,1)`, `(1,0,0,1)`.
- `N=5` (teto): um ladrilho só, `(0,0,0,0)` — liso dos quatro lados, encaixa consigo mesmo
  em qualquer direção e ladrilha o plano inteiro sozinho.

## Por que duas varreduras

A varredura com teto 3 leva **12 segundos**; com teto 5 leva **346**. A bateria roda a
barata, e isso só é legítimo porque nada morre entre 3 e 5 — as duas dão a mesma partição.

Esse é um argumento, e argumento não conferido é chute. Por isso o `test_pesados.py` refaz
a varredura de teto 5 inteira e **cobra a igualdade das duas partições**, em vez de confiar
na frase.

## A matriz de transferência

A busca na marra enche a grade célula a célula e refaz trabalho sem parar: a quinta coluna
não se importa com **como** as quatro primeiras ficaram, só com a cor que elas mostram para
a direita. Esse "só com" é a matriz de transferência.

Para uma altura fixa, uma coluna inteira se resume a dois perfis: o que ela mostra à
esquerda e o que mostra à direita. Monta-se

```
A[w][e] = quantas colunas válidas têm perfil oeste w e perfil leste e
```

e o número de ladrilhamentos de largura `m` é a **soma de todas as entradas de A^m**: cada
caminho `w₁ → e₁ = w₂ → e₂ = w₃ …` é um ladrilhamento, e as pontas ficam livres porque a
grade não tem borda obrigada.

Com `c` cores e altura `h` a matriz tem `c^h` linhas — **não** `|conjunto|^h`. Para `c=2` e
`h=5` são 32 linhas em vez de até 32.768.

## O que as medidas me corrigiram

- **Eu estimei o custo da varredura amostrando as 3.000 primeiras máscaras e errei por
  5×.** As primeiras máscaras são os conjuntos esparsos, que morrem rápido; os densos
  custam muito mais. Uma amostra uniforme deu 1,2 minuto, a rodada real levou 5,8 — e nem
  a uniforme acertou, porque a cauda de custo é pesada. Amostra enviesada pela ordem de
  enumeração é um jeito silencioso de errar estimativa.
- **Escrevi `alcancavel` com uma linha morta e a propagação errada.** Tinha um
  `(seguintes if False else set())` que não fazia nada e uma atribuição logo sobrescrita.
  Reescrevi com a recorrência explícita: depois de uma coluna valem todos os perfis leste
  da matriz, e cada coluna seguinte só pode começar onde a anterior terminou.
- **Meu teste de assimetria do encaixe não testava assimetria.** Peguei `(0,1,0,0)` e
  `(0,0,0,1)` para mostrar que A-depois-de-B difere de B-depois-de-A, mas nesse par a volta
  também casa, porque os dois valores em jogo são zero. O código estava certo e o teste é
  que estava errado. Troquei por um par de fato assimétrico.
- **Eu esperava achar conjuntos-armadilha.** A graça dos ladrilhos de Wang é justamente o
  conjunto que ladrilha uma região grande e trava depois. Com duas cores **não existe
  nenhum**: o buraco em 3 e 4 é total. O fenômeno precisa de mais cores, e isso a varredura
  disse, não o livro.

## Rodar

```bash
pip install -e ".[dev]"
pytest                               # a bateria inteira (o teto 5 leva ~6 min)
pytest --ignore=testes/test_pesados.py   # só a parte rápida
python -m wang                       # varredura com teto 3
python -m wang fundo                 # varredura com teto 5
python ferramentas/medidor.py --fundo
```

## Mapa

| arquivo | o que faz |
|---|---|
| `wang/nucleo.py` | ladrilhos, encaixe, grades |
| `wang/juiz.py` | ladrilhar na marra, célula por célula |
| `wang/busca.py` | a matriz de transferência |
| `wang/medidas.py` | as duas varreduras completas |
| `testes/test_pesados.py` | o achado central: ninguém morre em 3 nem em 4 |

25 testes. MIT.
