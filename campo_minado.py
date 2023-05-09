from prettytable import PrettyTable
import random
from copy import deepcopy
import os

matrizGabarito = []
matrizJogo = []
linhas = 8
colunas = 10
numBombas = 10
dicionario = {}


def lerArquivo():
    if not os.path.isfile("ranking.txt"):
        return

    with open("ranking.txt", "r") as arq:
        nomes = []
        for linha in arq:
            for nome in linha.split():
                if len(nome) >= 3:
                    nomes.append(nome)
        for nome in nomes:
            adicionarNome(nome)


def adicionarNome(nome):
    nome = nome.upper()
    num = dicionario.get(nome, None)
    # se nÃ£o existir a chave
    if num == None:
        # acrescenta uma chave no dicionario com valor 1
        dicionario[nome] = 1
    else:
        # se jÃ¡ existe, adiciona 1
        dicionario[nome] = num + 1


def salvaArquivo():
    with open("ranking.txt", "w") as arq:
        for nome, pontos in zip(dicionario.keys(), dicionario.values()):
            for i in range(int(pontos)):
                arq.write(f"{nome}\n")


def mostrarRanking():
    destaques = sorted(dicionario.items(),
                       key=lambda d: d[1], reverse=True)

    for i, (nome, pontos) in enumerate(destaques, start=1):
        print(f"{i}º: {nome} - {pontos} vitórias")
        if i == 20:
            break


def criarMatrizes(linhas, colunas):
    for i in range(linhas):
        novaLinhaGabarito = []
        novaLinhaJogo = []
        for j in range(colunas):
            novaLinhaGabarito.append(0)
            novaLinhaJogo.append("#")
        matrizGabarito.append(novaLinhaGabarito)
        matrizJogo.append(novaLinhaJogo)


def salvarValorNaMatrizGabarito(linha, coluna, valor):
    if matrizGabarito[linha][coluna] != -1:
        matrizGabarito[linha][coluna] = valor


def criarBomba(linhas, colunas):
    linha = random.randint(0, linhas-1)
    coluna = random.randint(0, colunas-1)

    existeBombaNaPosicao = matrizGabarito[linha][coluna] == -1
    if existeBombaNaPosicao:
        criarBomba(linhas, colunas)
    else:
        salvarValorNaMatrizGabarito(linha, coluna, -1)


def criarBombas(numBombas, linhas, colunas):
    for i in range(numBombas):
        criarBomba(linhas, colunas)


def preencherNumeros():
    for linha in range(len(matrizGabarito)):
        for coluna in range(len(matrizGabarito[linha])):
            if (matrizGabarito[linha][coluna] == -1):

                # primeiro passo > verificar esquerda e direita, soma 1
                if coluna > 0:
                    novoValor = matrizGabarito[linha][coluna-1] + 1
                    salvarValorNaMatrizGabarito(linha, coluna - 1, novoValor)

                if coluna < 9:
                    novoValor = matrizGabarito[linha][coluna+1] + 1
                    salvarValorNaMatrizGabarito(linha, coluna+1, novoValor)

            # segundo passo, linha de cima
                if linha > 0:
                    novoValor = matrizGabarito[linha-1][coluna] + 1
                    salvarValorNaMatrizGabarito(linha-1, coluna, novoValor)
                    if coluna > 0:
                        novoValor = matrizGabarito[linha - 1][coluna - 1] + 1
                        salvarValorNaMatrizGabarito(
                            linha-1, coluna-1, novoValor)
                    if coluna < 9:
                        novoValor = matrizGabarito[linha-1][coluna+1] + 1
                        salvarValorNaMatrizGabarito(
                            linha-1, coluna+1, novoValor)

                # terceiro passo, linha de baixo
                if linha < 7:
                    novoValor = matrizGabarito[linha+1][coluna] + 1
                    salvarValorNaMatrizGabarito(linha+1, coluna, novoValor)
                    if coluna > 0:
                        novoValor = matrizGabarito[linha+1][coluna-1] + 1
                        salvarValorNaMatrizGabarito(
                            linha+1, coluna-1, novoValor)
                    if coluna < 9:
                        novoValor = matrizGabarito[linha+1][coluna+1] + 1
                        salvarValorNaMatrizGabarito(
                            linha+1, coluna+1, novoValor)


def abrirMatriz(linha, coluna):
    for i in range(linha-1, linha+2):
        for j in range(coluna-1, coluna+2):
            if i >= 0 and i <= 7 and j >= 0 and j <= 9:
                x = matrizGabarito[i][j]
                if x == -1:
                    continue
                elif x == 0:
                    matrizJogo[i][j] = "//"
                    matrizGabarito[i][j] = "//"
                    abrirMatriz(i, j)
                else:
                    matrizJogo[i][j] = matrizGabarito[i][j]


def verificaSeGanhou():
    contador = 0
    for linha in range(len(matrizJogo)):
        for coluna in range(len(matrizJogo[linha])):
            if matrizJogo[linha][coluna] == '#':
                contador = contador + 1
    if contador == numBombas:
        return True
    return False


def campoJogo():
    nomes = [""]
    campoJogo = deepcopy(matrizJogo)
    for i in range(linhas):
        campoJogo[i].insert(0, f'linha {i}')

    for i in range(colunas):
        nomes.append(f'coluna {i}')
    tabelaJogo = PrettyTable()
    tabelaJogo.field_names = nomes
    # print(matrizJogo)
    # print(campoJogo)
    tabelaJogo.add_rows(campoJogo)
    print(tabelaJogo)


def inciarJogo(nome):
    while (True):
        campoJogo()
        if verificaSeGanhou():
            print('PARABENS! VOCE GANHOU!')
            adicionarNome(nome)
            break
        posicao = input('Numero separados por espacos: ').split(' ')
        linha = int(posicao[0])
        coluna = int(posicao[1])

        if matrizGabarito[linha][coluna] == 0:
            abrirMatriz(linha, coluna)
        elif matrizGabarito[linha][coluna] != -1:
            matrizJogo[linha][coluna] = matrizGabarito[linha][coluna]
        else:
            print('KABOOM')
            break

# tabelaGabarito = PrettyTable()
# tabelaGabarito.add_rows(matrizGabarito)
# print(tabelaGabarito)


lerArquivo()

while True:
    print()
    print("JOGO CAMPO MINADO")
    print()
    print("1. INICIAR JOGO")
    print("2. VER RANKING")
    print("3. SAIR")
    print("")
    opcao = int(input("Digite a opcao buscada: "))
    if opcao == 1:
        criarMatrizes(linhas, colunas)
        criarBombas(numBombas, linhas, colunas)
        preencherNumeros()
        nome = input('QUAL O NOME DO JOGADOR: ')
        inciarJogo(nome)
    elif opcao == 2:
        mostrarRanking()
    elif opcao == 3:
        salvaArquivo()
        break
    else:
        salvaArquivo()
        break
